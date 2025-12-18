import streamlit as st
import os
import subprocess
import tempfile
from pathlib import Path
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
import time
from datetime import datetime
import json

# ページ設定
st.set_page_config(
    page_title="リアルタイム文字起こしと翻訳",
    page_icon="🎙️",
    layout="wide"
)

# セッション状態の初期化
if 'transcription_done' not in st.session_state:
    st.session_state.transcription_done = False
if 'segments' not in st.session_state:
    st.session_state.segments = []
if 'translated_segments' not in st.session_state:
    st.session_state.translated_segments = []
if 'realtime_mode' not in st.session_state:
    st.session_state.realtime_mode = False
if 'realtime_subtitles' not in st.session_state:
    st.session_state.realtime_subtitles = []
if 'whisper_model' not in st.session_state:
    st.session_state.whisper_model = None
if 'auto_transcribe' not in st.session_state:
    st.session_state.auto_transcribe = False
if 'realtime_transcribe' not in st.session_state:
    st.session_state.realtime_transcribe = False
if 'last_audio_hash' not in st.session_state:
    st.session_state.last_audio_hash = None
if 'realtime_subtitles_list' not in st.session_state:
    st.session_state.realtime_subtitles_list = []
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'recording_chunks' not in st.session_state:
    st.session_state.recording_chunks = []
if 'processed_chunks' not in st.session_state:
    st.session_state.processed_chunks = 0
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'stop_processing' not in st.session_state:
    st.session_state.stop_processing = False

# タイトル
st.title("🎙️ リアルタイム文字起こしと翻訳アプリ")
st.markdown("---")

# サイドバー：設定
with st.sidebar:
    st.header("⚙️ 設定")
    
    model_size = st.selectbox(
        "Whisperモデルサイズ",
        ["tiny", "base", "small", "medium", "large"],
        index=2,
        help="大きいほど精度が高いですが、処理が遅くなります"
    )
    
    compute_type = st.selectbox(
        "計算タイプ",
        ["int8", "float16", "float32"],
        index=0,
        help="int8が最も高速ですが、精度はやや低いです"
    )
    
    display_interval = st.slider(
        "字幕表示間隔（秒）",
        min_value=1,
        max_value=10,
        value=3,
        help="字幕を更新する間隔"
    )
    
    st.markdown("---")
    st.markdown("### 📝 使い方")
    st.markdown("""
    **ファイルアップロード:**
    1. 音声ファイルをアップロード
    2. 「文字起こし開始」ボタンをクリック
    3. 字幕が表示されます
    
    **マイク入力:**
    1. 「マイクから録音」タブを選択
    2. 録音ボタンをクリック
    3. リアルタイムで文字起こし・翻訳
    """)

# タブでファイルアップロードとマイク入力を切り替え
tab1, tab2 = st.tabs(["📁 ファイルアップロード", "🎤 マイクから録音"])

with tab1:
    # メインエリア
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📁 音声ファイルのアップロード")
        uploaded_file = st.file_uploader(
            "音声ファイルを選択してください",
            type=['wav', 'mp3', 'm4a', 'flac', 'ogg', 'webm'],
            help="対応形式: WAV, MP3, M4A, FLAC, OGG, WEBM"
        )

    with col2:
        st.header("🎯 言語検出")
        auto_detect = st.checkbox("自動検出", value=True)
        if not auto_detect:
            source_lang = st.selectbox(
                "音声の言語",
                ["ja", "en"],
                format_func=lambda x: "日本語" if x == "ja" else "英語"
            )
        else:
            source_lang = None

with tab2:
    st.header("🎤 マイクからリアルタイム録音")
    st.info("💡 マイクの使用許可をブラウザで許可してください")
    
    # 自動文字起こしの設定
    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        auto_transcribe = st.checkbox("🎯 録音完了後に自動で文字起こし・翻訳を実行", value=st.session_state.auto_transcribe)
        st.session_state.auto_transcribe = auto_transcribe
    with col_mode2:
        realtime_transcribe = st.checkbox("⚡ 録音中リアルタイム字幕表示", value=st.session_state.realtime_transcribe)
        st.session_state.realtime_transcribe = realtime_transcribe
        if realtime_transcribe:
            st.caption("録音完了後、短いチャンクに分割して順次処理し、字幕をリアルタイムで表示します")
    
    # リアルタイム字幕表示モードの場合、字幕エリアを事前に表示
    if st.session_state.realtime_transcribe:
        st.markdown("### 📺 リアルタイム字幕")
        st.markdown("---")
        subtitle_display_realtime = st.empty()
        
        # 停止ボタン
        if st.session_state.is_processing:
            if st.button("⏹️ 字幕処理を停止", type="secondary", use_container_width=True):
                st.session_state.stop_processing = True
                st.session_state.is_processing = False
                st.rerun()
    
    # マイク入力
    audio_data = st.audio_input("音声を録音してください", label_visibility="collapsed")
    
    # 録音が検知された瞬間に処理開始フラグを設定
    if audio_data is not None and st.session_state.realtime_transcribe:
        if not st.session_state.is_processing:
            st.session_state.is_processing = True
            st.session_state.stop_processing = False
    
    if audio_data is not None:
        # 音声データのハッシュを計算（同じ音声の重複処理を防ぐ）
        import hashlib
        audio_bytes = audio_data.read()
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        audio_data.seek(0)  # ポインタをリセット
        
        # 新しい音声の場合のみ処理
        if st.session_state.last_audio_hash != audio_hash:
            # 録音された音声を一時ファイルに保存
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_audio:
                tmp_audio.write(audio_data.read())
                mic_audio_path = tmp_audio.name
            
            # 16kHz mono WAVに変換
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_wav:
                audio_wav_path = tmp_wav.name
            
            try:
                # ffmpegで変換
                cmd = [
                    "ffmpeg", "-y", "-i", mic_audio_path,
                    "-ac", "1", "-ar", "16000", audio_wav_path
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    st.error(f"音声変換エラー: {result.stderr}")
                else:
                    st.success("✅ 録音完了！")
                    
                    # リアルタイム字幕表示モード
                    if st.session_state.realtime_transcribe and not st.session_state.stop_processing:
                        # 処理開始を表示
                        with subtitle_display_realtime.container():
                            st.info("🔄 録音完了！字幕処理を開始します...")
                        
                        # 音声を短いチャンクに分割して処理
                        try:
                            # Whisperモデルの読み込み
                            if st.session_state.whisper_model is None:
                                with st.spinner("モデルを読み込み中..."):
                                    st.session_state.whisper_model = WhisperModel(
                                        model_size,
                                        device="cpu",
                                        compute_type=compute_type
                                    )
                            
                            model = st.session_state.whisper_model
                            
                            # 音声の長さを取得
                            import wave
                            with wave.open(audio_wav_path, 'rb') as wav_file:
                                frames = wav_file.getnframes()
                                sample_rate = wav_file.getframerate()
                                duration = frames / float(sample_rate)
                            
                            # チャンクサイズ（秒）- より短くしてリアルタイム感を向上
                            chunk_size = 2.0
                            all_subtitles = []
                            detected_lang = None
                            
                            # プログレスバー
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            # チャンクごとに処理
                            num_chunks = int(duration / chunk_size) + (1 if duration % chunk_size > 0 else 0)
                            
                            # 字幕をクリア
                            all_subtitles_display = []
                            
                            for chunk_idx, chunk_start in enumerate(range(0, int(duration), int(chunk_size))):
                                # 停止フラグをチェック
                                if st.session_state.stop_processing:
                                    st.warning("⏹️ 字幕処理が停止されました")
                                    break
                                
                                chunk_end = min(chunk_start + chunk_size, duration)
                                
                                # プログレス更新
                                progress = (chunk_idx + 1) / num_chunks
                                progress_bar.progress(progress)
                                status_text.text(f"処理中: {chunk_start:.1f}s - {chunk_end:.1f}s ({chunk_idx + 1}/{num_chunks})")
                                
                                # チャンクを抽出
                                chunk_wav_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
                                cmd_chunk = [
                                    "ffmpeg", "-y", "-i", audio_wav_path,
                                    "-ss", str(chunk_start), "-t", str(chunk_size),
                                    "-ac", "1", "-ar", "16000", chunk_wav_path
                                ]
                                subprocess.run(cmd_chunk, capture_output=True, text=True)
                                
                                # 文字起こし
                                try:
                                    segments, info = model.transcribe(
                                        chunk_wav_path,
                                        language=source_lang,
                                        vad_filter=True
                                    )
                                    segments_list = list(segments)
                                    
                                    if not detected_lang:
                                        detected_lang = info.language
                                    
                                    # 翻訳
                                    if segments_list:
                                        # 言語に応じて翻訳先を決定
                                        if detected_lang == "ja":
                                            target_lang = "en"
                                            source_name = "日本語"
                                            target_name = "英語"
                                        elif detected_lang == "en":
                                            target_lang = "ja"
                                            source_name = "英語"
                                            target_name = "日本語"
                                        else:
                                            # その他の言語は英語に翻訳
                                            target_lang = "en"
                                            source_name = detected_lang.upper()
                                            target_name = "英語"
                                        
                                        # 翻訳器を初期化（各チャンクで再初期化）
                                        translator = GoogleTranslator(source=detected_lang, target=target_lang)
                                        
                                        for seg in segments_list:
                                            text = seg.text.strip()
                                            if not text:
                                                continue
                                            
                                            try:
                                                # 翻訳実行
                                                translated_text = translator.translate(text)
                                                
                                                # 翻訳結果が空でないか確認
                                                if not translated_text or translated_text.strip() == "":
                                                    translated_text = text  # 翻訳失敗時は元のテキスト
                                                
                                                subtitle_item = {
                                                    'start': chunk_start + seg.start,
                                                    'end': chunk_start + seg.end,
                                                    'original': text,
                                                    'translated': translated_text,
                                                    'source_name': source_name,
                                                    'target_name': target_name
                                                }
                                                all_subtitles.append(subtitle_item)
                                                all_subtitles_display.append(subtitle_item)
                                                
                                                # リアルタイムで字幕を表示（累積的に）
                                                with subtitle_display_realtime.container():
                                                    for sub in all_subtitles_display:
                                                        st.markdown(f"**[{sub['start']:.1f}s - {sub['end']:.1f}s]**")
                                                        st.markdown(f"**{sub['source_name']}:** {sub['original']}")
                                                        st.markdown(f"**{sub['target_name']}:** {sub['translated']}")
                                                        st.markdown("---")
                                                
                                                time.sleep(0.05)  # API制限を避ける（短縮）
                                            except Exception as e:
                                                # エラー時は元のテキストを表示
                                                st.warning(f"翻訳エラー: {str(e)} | テキスト: {text[:50]}")
                                                subtitle_item = {
                                                    'start': chunk_start + seg.start,
                                                    'end': chunk_start + seg.end,
                                                    'original': text,
                                                    'translated': text,  # エラー時は元のテキスト
                                                    'source_name': source_name,
                                                    'target_name': target_name
                                                }
                                                all_subtitles.append(subtitle_item)
                                                all_subtitles_display.append(subtitle_item)
                                                
                                                # エラー時も字幕を表示
                                                with subtitle_display_realtime.container():
                                                    for sub in all_subtitles_display:
                                                        st.markdown(f"**[{sub['start']:.1f}s - {sub['end']:.1f}s]**")
                                                        st.markdown(f"**{sub['source_name']}:** {sub['original']}")
                                                        if sub['translated'] == sub['original'] and sub['original']:
                                                            st.markdown(f"**{sub['target_name']}:** {sub['translated']} ⚠️ (翻訳エラー)")
                                                        else:
                                                            st.markdown(f"**{sub['target_name']}:** {sub['translated']}")
                                                        st.markdown("---")
                                
                                except Exception as e:
                                    st.warning(f"チャンク {chunk_start:.1f}s-{chunk_end:.1f}s の処理でエラー: {str(e)}")
                                
                                finally:
                                    try:
                                        os.unlink(chunk_wav_path)
                                    except:
                                        pass
                            
                            # プログレスバーをクリア
                            progress_bar.empty()
                            status_text.empty()
                            
                            # 処理完了
                            st.session_state.is_processing = False
                            
                            # 最終結果をセッション状態に保存
                            if all_subtitles:
                                st.session_state.realtime_subtitles_list = all_subtitles
                                st.session_state.translated_segments = all_subtitles
                                st.session_state.segments = [type('obj', (object,), {
                                    'start': s['start'],
                                    'end': s['end'],
                                    'text': s['original']
                                })() for s in all_subtitles]
                                st.session_state.detected_language = detected_lang
                                st.session_state.transcription_done = True
                                
                                with subtitle_display_realtime.container():
                                    st.success(f"✅ リアルタイム字幕処理完了！検出言語: {detected_lang} | 合計 {len(all_subtitles)} セグメント")
                            
                            st.session_state.last_audio_hash = audio_hash
                            
                        except Exception as e:
                            st.session_state.is_processing = False
                            st.error(f"リアルタイム処理エラー: {str(e)}")
                    
                    # 自動文字起こしが有効な場合、自動実行
                    elif st.session_state.auto_transcribe:
                        with st.spinner("🔄 自動で文字起こし・翻訳を実行中..."):
                            try:
                                # Whisperモデルの読み込み（キャッシュがあれば再利用）
                                if st.session_state.whisper_model is None:
                                    st.session_state.whisper_model = WhisperModel(
                                        model_size,
                                        device="cpu",
                                        compute_type=compute_type
                                    )
                                
                                model = st.session_state.whisper_model
                                
                                # 文字起こし実行
                                segments, info = model.transcribe(
                                    audio_wav_path,
                                    language=source_lang,
                                    vad_filter=True
                                )
                                
                                segments_list = list(segments)
                                st.session_state.segments = segments_list
                                st.session_state.detected_language = info.language
                                st.session_state.transcription_done = True
                                
                                # 自動翻訳も実行
                                if segments_list:
                                    detected_lang = info.language
                                    if detected_lang == "ja":
                                        target_lang = "en"
                                        source_name = "日本語"
                                        target_name = "英語"
                                    elif detected_lang == "en":
                                        target_lang = "ja"
                                        source_name = "英語"
                                        target_name = "日本語"
                                    else:
                                        # その他の言語は英語に翻訳
                                        target_lang = "en"
                                        source_name = detected_lang.upper()
                                        target_name = "英語"
                                    
                                    translator = GoogleTranslator(source=detected_lang, target=target_lang)
                                    translated = []
                                    
                                    for seg in segments_list:
                                        text = seg.text.strip()
                                        if not text:
                                            continue
                                        try:
                                            translated_text = translator.translate(text)
                                            # 翻訳結果が空でないか確認
                                            if not translated_text or translated_text.strip() == "":
                                                translated_text = text
                                            translated.append({
                                                'start': seg.start,
                                                'end': seg.end,
                                                'original': text,
                                                'translated': translated_text
                                            })
                                            time.sleep(0.1)  # API制限を避ける
                                        except Exception as e:
                                            st.warning(f"翻訳エラー: {str(e)} | テキスト: {text[:50]}")
                                            translated.append({
                                                'start': seg.start,
                                                'end': seg.end,
                                                'original': text,
                                                'translated': text
                                            })
                                    
                                    st.session_state.translated_segments = translated
                                
                                st.session_state.last_audio_hash = audio_hash
                                st.success(f"✅ 文字起こし・翻訳完了！検出言語: {info.language}")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"文字起こしエラー: {str(e)}")
                    else:
                        # 手動実行モード
                        col_btn1, col_btn2 = st.columns(2)
                        
                        with col_btn1:
                            if st.button("🚀 文字起こし開始", type="primary", use_container_width=True):
                                with st.spinner("文字起こしを実行中..."):
                                    try:
                                        # Whisperモデルの読み込み（キャッシュがあれば再利用）
                                        if st.session_state.whisper_model is None:
                                            st.session_state.whisper_model = WhisperModel(
                                                model_size,
                                                device="cpu",
                                                compute_type=compute_type
                                            )
                                        
                                        model = st.session_state.whisper_model
                                        
                                        # 文字起こし実行
                                        segments, info = model.transcribe(
                                            audio_wav_path,
                                            language=source_lang,
                                            vad_filter=True
                                        )
                                        
                                        segments_list = list(segments)
                                        st.session_state.segments = segments_list
                                        st.session_state.detected_language = info.language
                                        st.session_state.transcription_done = True
                                        st.session_state.last_audio_hash = audio_hash
                                        
                                        st.success(f"✅ 文字起こし完了！検出言語: {info.language}")
                                        st.rerun()
                                        
                                    except Exception as e:
                                        st.error(f"文字起こしエラー: {str(e)}")
                        
                        with col_btn2:
                            if st.button("🔄 再録音", use_container_width=True):
                                st.session_state.transcription_done = False
                                st.session_state.last_audio_hash = None
                                st.rerun()
                    
                    # 録音された音声を再生
                    st.audio(audio_data, format="audio/wav")
                
                # ハッシュを更新
                st.session_state.last_audio_hash = audio_hash
            
            except Exception as e:
                st.error(f"エラー: {str(e)}")
            finally:
                # 一時ファイルのクリーンアップ
                try:
                    os.unlink(mic_audio_path)
                except:
                    pass

# ファイルアップロードの文字起こし処理
if uploaded_file is not None:
    # 一時ファイルに保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_audio_path = tmp_file.name
    
    # 16kHz mono WAVに変換
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_wav:
        audio_wav_path = tmp_wav.name
    
    try:
        # ffmpegで変換
        cmd = [
            "ffmpeg", "-y", "-i", tmp_audio_path,
            "-ac", "1", "-ar", "16000", audio_wav_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            st.error(f"音声変換エラー: {result.stderr}")
        else:
            st.success("✅ 音声ファイルの準備が完了しました")
            
            if st.button("🚀 文字起こし開始", type="primary", use_container_width=True):
                with st.spinner("文字起こしを実行中..."):
                    try:
                        # Whisperモデルの読み込み（キャッシュがあれば再利用）
                        if st.session_state.whisper_model is None:
                            st.session_state.whisper_model = WhisperModel(
                                model_size,
                                device="cpu",
                                compute_type=compute_type
                            )
                        model = st.session_state.whisper_model
                        
                        # 文字起こし実行
                        segments, info = model.transcribe(
                            audio_wav_path,
                            language=source_lang,
                            vad_filter=True
                        )
                        
                        segments_list = list(segments)
                        st.session_state.segments = segments_list
                        st.session_state.detected_language = info.language
                        st.session_state.transcription_done = True
                        
                        st.success(f"✅ 文字起こし完了！検出言語: {info.language}")
                        
                    except Exception as e:
                        st.error(f"文字起こしエラー: {str(e)}")
    
    except Exception as e:
        st.error(f"エラー: {str(e)}")
    finally:
        # 一時ファイルのクリーンアップ
        try:
            os.unlink(tmp_audio_path)
        except:
            pass

# 字幕表示と翻訳
if st.session_state.transcription_done and st.session_state.segments:
    st.markdown("---")
    st.header("📺 字幕表示")
    
    # 翻訳の設定
    detected_lang = st.session_state.detected_language
    if detected_lang == "ja":
        target_lang = "en"
        source_name = "日本語"
        target_name = "英語"
    elif detected_lang == "en":
        target_lang = "ja"
        source_name = "英語"
        target_name = "日本語"
    else:
        # その他の言語は英語に翻訳
        target_lang = "en"
        source_name = detected_lang.upper()
        target_name = "英語"
    
    st.info(f"🔍 検出された言語: {source_name} → 翻訳先: {target_name}")
    
    # 翻訳実行
    if st.button("🌐 翻訳を実行", use_container_width=True):
        translator = GoogleTranslator(source=detected_lang, target=target_lang)
        translated = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, seg in enumerate(st.session_state.segments):
            text = seg.text.strip()
            if not text:
                continue
            
            try:
                # 翻訳実行
                translated_text = translator.translate(text)
                
                # 翻訳結果が空でないか確認
                if not translated_text or translated_text.strip() == "":
                    translated_text = text
                
                translated.append({
                    'start': seg.start,
                    'end': seg.end,
                    'original': text,
                    'translated': translated_text
                })
                
                progress_bar.progress((i + 1) / len(st.session_state.segments))
                status_text.text(f"翻訳中: {i + 1}/{len(st.session_state.segments)} | {source_name}→{target_name}")
                
                # API制限を避けるため、少し待機
                time.sleep(0.1)
                
            except Exception as e:
                st.warning(f"翻訳エラー（セグメント {i+1}）: {str(e)} | テキスト: {text[:50]}")
                translated.append({
                    'start': seg.start,
                    'end': seg.end,
                    'original': text,
                    'translated': text  # エラー時は元のテキスト
                })
        
        st.session_state.translated_segments = translated
        progress_bar.empty()
        status_text.empty()
        st.success("✅ 翻訳完了！")
    
    # 字幕表示エリア
    if st.session_state.translated_segments:
        st.markdown("### 🎬 リアルタイム字幕プレビュー")
        
        # 字幕表示用のコンテナ
        subtitle_container = st.container()
        
        # 再生位置（秒）
        current_time = st.slider(
            "再生位置（秒）",
            min_value=0.0,
            max_value=float(st.session_state.segments[-1].end) if st.session_state.segments else 100.0,
            value=0.0,
            step=0.1
        )
        
        # 現在の字幕を表示
        current_subtitle = None
        for item in st.session_state.translated_segments:
            if item['start'] <= current_time <= item['end']:
                current_subtitle = item
                break
        
        if current_subtitle:
            subtitle_container.markdown("---")
            subtitle_container.markdown(f"### 🎯 現在の字幕")
            subtitle_container.markdown(f"**{source_name}:** {current_subtitle['original']}")
            subtitle_container.markdown(f"**{target_name}:** {current_subtitle['translated']}")
            subtitle_container.markdown(f"*時間: {current_subtitle['start']:.1f}s - {current_subtitle['end']:.1f}s*")
        
        # 全字幕リスト
        with st.expander("📋 全字幕リストを表示"):
            for i, item in enumerate(st.session_state.translated_segments, 1):
                st.markdown(f"**{i}. [{item['start']:.1f}s - {item['end']:.1f}s]**")
                st.markdown(f"- {source_name}: {item['original']}")
                st.markdown(f"- {target_name}: {item['translated']}")
                st.markdown("---")
        
        # SRTファイル生成
        st.markdown("---")
        st.header("💾 字幕ファイルのダウンロード")
        
        def generate_srt(segments_data, include_translation=True):
            """SRTファイルを生成"""
            srt_content = ""
            idx = 1
            
            for item in segments_data:
                if not item['original'].strip():
                    continue
                
                # 時間フォーマット変換
                def srt_time(sec):
                    h = int(sec // 3600)
                    m = int((sec % 3600) // 60)
                    s = int(sec % 60)
                    ms = int((sec - int(sec)) * 1000)
                    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
                
                start_time = srt_time(item['start'])
                end_time = srt_time(item['end'])
                
                # 字幕テキスト
                if include_translation:
                    subtitle_text = f"{item['original']}\n{item['translated']}"
                else:
                    subtitle_text = item['original']
                
                srt_content += f"{idx}\n{start_time} --> {end_time}\n{subtitle_text}\n\n"
                idx += 1
            
            return srt_content
        
        col_dl1, col_dl2 = st.columns(2)
        
        with col_dl1:
            # 翻訳付きSRT
            srt_with_translation = generate_srt(st.session_state.translated_segments, include_translation=True)
            st.download_button(
                label="📥 翻訳付きSRTをダウンロード",
                data=srt_with_translation,
                file_name="subtitles_with_translation.srt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_dl2:
            # 元の言語のみSRT
            srt_original = generate_srt(st.session_state.translated_segments, include_translation=False)
            st.download_button(
                label="📥 元の言語のみSRTをダウンロード",
                data=srt_original,
                file_name="subtitles_original.srt",
                mime="text/plain",
                use_container_width=True
            )
        
        # JSON形式でもダウンロード可能
        json_data = json.dumps(st.session_state.translated_segments, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 JSON形式でダウンロード",
            data=json_data,
            file_name="subtitles.json",
            mime="application/json",
            use_container_width=True
        )

# フッター
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>リアルタイム文字起こしと翻訳アプリ | faster-whisper + deep-translator</p>
    <p>アカウント不要・課金不要</p>
</div>
""", unsafe_allow_html=True)

