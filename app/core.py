import json
import genanki
import os
import datetime
import glob
import requests
import hashlib
from dotenv import load_dotenv, set_key

class AnkiGenerator:
    def __init__(self, data_dir='data', output_dir='output', env_path='.env'):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.env_path = env_path
        self.words_file = os.path.join(data_dir, 'words.json')
        self.others_file = os.path.join(data_dir, 'others.json')
        self.state_file = os.path.join(data_dir, '.state.json')
        
        load_dotenv(self.env_path)
        self.discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        self.model_id_words = 1776685003402
        self.deck_id_words = 1
        self.model_id_others = 1776685003403
        self.deck_id_others = 2
        
        self.model_words = genanki.Model(
            self.model_id_words,
            'Basic (Automated Compatibility)',
            fields=[{'name': 'Front'}, {'name': 'Back'}],
            templates=[{
                'name': 'Card 1',
                'qfmt': '<div class="term">{{Front}}</div>',
                'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
            }],
            css=self._get_css()
        )

        self.model_others = genanki.Model(
            self.model_id_others,
            'Basic (General)',
            fields=[{'name': 'Front'}, {'name': 'Back'}],
            templates=[{
                'name': 'Card 1',
                'qfmt': '<div class="term">{{Front}}</div>',
                'afmt': '{{FrontSide}}<hr id="answer"><div class="meaning">{{Back}}</div>',
            }],
            css=self._get_css()
        )

    def _get_css(self):
        return '''
.card {
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 20px;
    text-align: center;
    color: #212121;
    background-color: #ffffff;
    line-height: 1.6;
    padding: 20px;
}
.nightMode.card { color: #e0e0e0; background-color: #121212; }
.term { font-size: 32px; font-weight: bold; color: #007bff; margin-bottom: 12px; }
.nightMode .term { color: #90caf9; }
.pos { color: #d32f2f; font-weight: bold; font-style: italic; margin-right: 8px; }
.nightMode .pos { color: #ef9a9a; }
.meaning { font-size: 24px; font-weight: 500; }
.example-box {
    background-color: #f5f5f5;
    border-left: 5px solid #007bff;
    padding: 12px;
    margin-top: 20px;
    text-align: left;
    border-radius: 4px;
}
.nightMode .example-box {
    background-color: #1e1e1e;
    border-left: 5px solid #90caf9;
    color: #e0e0e0;
}
'''

    def get_file_hash(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_state(self, hash_val, filename):
        state = {'last_hash': hash_val, 'last_file': filename}
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)

    def update_webhook(self, url):
        self.discord_webhook_url = url
        set_key(self.env_path, 'DISCORD_WEBHOOK_URL', url)

    def read_json(self, target="words"):
        target_file = self.words_file if target == "words" else self.others_file
        if not os.path.exists(target_file):
            return "{\n\n}"
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def save_json(self, content, target="words"):
        target_file = self.words_file if target == "words" else self.others_file
        try:
            # Validate JSON
            parsed = json.loads(content)
            # Try to format it out nicely when saving back
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(formatted)
            return True, "JSON saved successfully!"
        except json.JSONDecodeError as e:
            return False, f"JSON Syntax Error: {e.msg} at line {e.lineno}"
        except Exception as e:
            return False, f"Error saving file: {e}"

    def send_to_discord(self, file_path, prefix=""):
        if not self.discord_webhook_url:
            return "Discord Webhook URL is not set."

        msg = f"{prefix}New Anki deck ready: {os.path.basename(file_path)}"
        payload = {"content": msg}
        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                response = requests.post(self.discord_webhook_url, data=payload, files=files)
            
            if response.status_code in [200, 204]:
                return f"Success: Sent to Discord ({prefix.strip()})"
            else:
                return f"Error: Discord failed with code {response.status_code}"
        except Exception as e:
            return f"Error: Discord error {e}"

    def cleanup_old_files(self, days=7):
        now = datetime.datetime.now()
        cutoff = now - datetime.timedelta(days=days)
        files = glob.glob(os.path.join(self.output_dir, "*.apkg"))
        count = 0
        for f in files:
            if datetime.datetime.fromtimestamp(os.path.getmtime(f)) < cutoff:
                try:
                    os.remove(f)
                    count += 1
                except: pass
        return count

    def generate(self, log_callback=None):
        def log(msg):
            if log_callback: log_callback(msg)
            else: print(msg)

        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        has_words = os.path.exists(self.words_file)
        has_others = os.path.exists(self.others_file)

        if not has_words and not has_others:
            return False, f"Error: No data files found."

        data_words = {}
        if has_words:
            try:
                with open(self.words_file, mode='r', encoding='utf-8') as f:
                    data_words = json.load(f)
            except: pass

        data_others = {}
        if has_others:
            try:
                with open(self.others_file, mode='r', encoding='utf-8') as f:
                    data_others = json.load(f)
            except: pass

        words_hash = self.get_file_hash(self.words_file) if has_words else ""
        others_hash = self.get_file_hash(self.others_file) if has_others else ""
        current_hash = hashlib.md5((words_hash + others_hash).encode()).hexdigest()

        state = self.load_state()
        last_hash = state.get('last_hash')
        last_file = state.get('last_file')
        
        is_unchanged = (current_hash == last_hash) and last_file and os.path.exists(os.path.join(self.output_dir, last_file))
        
        if is_unchanged:
            filename = last_file
            status_msg = " (No changes detected - Overwriting)"
            discord_prefix = "[No Changes] "
        else:
            first_key = "deck"
            if data_words:
                first_key = next(iter(data_words.keys()))
            elif data_others:
                first_key = next(iter(data_others.keys()))
            
            safe_word = "".join(x for x in first_key if x.isalnum() or x in " -_").strip()
            timestamp = datetime.datetime.now().strftime("%m%d%Y")
            filename = f"{timestamp}_{safe_word}.apkg"
            status_msg = ""
            discord_prefix = "[New] "

        output_path = os.path.join(self.output_dir, filename)
        
        decks = []

        if data_words:
            my_deck_words = genanki.Deck(self.deck_id_words, 'English Words')
            for word, details in data_words.items():
                reading = details.get('reading', '')
                pos = details.get('pos', '')
                meaning = details.get('meaning', '')
                synonyms = details.get('synonyms', '')
                example = details.get('example', '')
                tags = details.get('tags', [])

                back_html = f'''
<div style="margin-bottom: 8px;">
    <span style="font-size: 0.8em; color: #757575;">{reading}</span>
</div>
<div class="meaning">
    <span class="pos">{pos}</span> {meaning}
</div>
<div style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">
    Synonyms: {synonyms}
</div>
<div class="example-box">
    <i>{example}</i>
</div>
'''
                my_note = genanki.Note(
                    model=self.model_words,
                    fields=[word, back_html],
                    tags=tags
                )
                my_deck_words.add_note(my_note)
            decks.append(my_deck_words)

        if data_others:
            my_deck_others = genanki.Deck(self.deck_id_others, 'General Items')
            for item, details in data_others.items():
                if isinstance(details, str):
                    back_html = details
                    tags = []
                elif isinstance(details, dict):
                    back_html = details.get('back', details.get('meaning', ''))
                    tags = details.get('tags', [])
                else:
                    back_html = str(details)
                    tags = []

                my_note = genanki.Note(
                    model=self.model_others,
                    fields=[item, back_html],
                    tags=tags
                )
                my_deck_others.add_note(my_note)
            decks.append(my_deck_others)

        if not decks:
            return False, "No valid data to generate deck."

        try:
            genanki.Package(decks).write_to_file(output_path)
            log(f"Generated: {filename}{status_msg}")
            
            self.save_state(current_hash, filename)
            discord_res = self.send_to_discord(output_path, discord_prefix)
            log(discord_res)
            
            cleaned = self.cleanup_old_files(days=7)
            if cleaned > 0: log(f"Cleaned up {cleaned} old files.")
            
            return True, f"Success: {filename} generated."
        except Exception as e:
            return False, f"Error: {e}"

    def get_word_count(self):
        count = 0
        if os.path.exists(self.words_file):
            try:
                with open(self.words_file, 'r', encoding='utf-8') as f:
                    count += len(json.load(f))
            except: pass
        if os.path.exists(self.others_file):
            try:
                with open(self.others_file, 'r', encoding='utf-8') as f:
                    count += len(json.load(f))
            except: pass
        return count

    def get_recent_files(self, limit=5):
        files = glob.glob(os.path.join(self.output_dir, "*.apkg"))
        files.sort(key=os.path.getmtime, reverse=True)
        return [os.path.basename(f) for f in files[:limit]]
