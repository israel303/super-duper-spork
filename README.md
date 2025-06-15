# Telegram Thumbnail Bot 📄

בוט טלגרם שמוסיף תמונת thumbnail קבועה לקבצי PDF ו־EPUB שנשלחים אליו, ומחזיר אותם עם הכיתוב "Oldtown".

## איך זה עובד?
1. שלח לבוט קובץ PDF או EPUB 📤
2. הוא יוסיף לו thumbnail קבוע (שמוגדר מראש)
3. תקבל את הקובץ בחזרה עם הכיתוב: "📄 הנה הקובץ שלך עם כיתוב Oldtown."

## קבצי המערכת:
- `main.py` – קוד הבוט
- `requirements.txt` – ספריות נדרשות להתקנה
- `default_thumb.jpg` – תמונה שתשמש כ-thumbnail קבוע
- `README.md` – מדריך זה

## משתני סביבה (Render או מקומית)
- `BOT_TOKEN` – טוקן של בוט טלגרם שלך

## התקנה מקומית (אם לא מרנדר)
```bash
pip install -r requirements.txt
python main.py
```

בהצלחה! 🚀
