(
echo AzureAPI=
echo MistralAPI=
) > .env

python -m venv ./venv
call venv\Scripts\activate && pip install -r requirements.txt

:choice
set /p mode=Enter mode (prompt/voice):
if /i "%mode%"=="prompt" goto prompt_mode
if /i "%mode%"=="voice" goto voice_mode
echo Invalid input. Please enter "prompt" or "voice".
goto choice

:prompt_mode
python runner.py
goto end

:voice_mode
python runner.py --stt
goto end

:end
pause