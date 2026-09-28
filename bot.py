import os
import telebot
import google.generativeai as genai
from dotenv import load_dotenv
from analyzer import RealEstateAnalyzer

# 1. تحميل المتغيرات من .env
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
BOT_PASSWORD = os.getenv("BOT_PASSWORD")

if not all([BOT_TOKEN, GEMINI_KEY, BOT_PASSWORD]):
    raise ValueError("❌ تأكد من إضافة المتغيرات الثلاثة في ملف .env")

BOT_TOKEN = BOT_TOKEN.replace('"', '').strip()
GEMINI_KEY = GEMINI_KEY.replace('"', '').strip()
BOT_PASSWORD = BOT_PASSWORD.replace('"', '').strip()

# 2. تهيئة جيميناي (الإصدار الأحدث)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-3.8-flash')

# 3. تهيئة البوت والمحلل العقاري
bot = telebot.TeleBot(BOT_TOKEN)
print("⏳ جاري تشغيل البوت وربطه بالمحلل العقاري...")
analyzer = RealEstateAnalyzer()

authenticated_users = set()


def get_gemini_advice(city, district, analysis_result):
    """
    توليد نصيحة متزنة تستخدم مصطلحات عامية (ماش، مو ذاك الزود)
    وتعتبر بيانات مارس 2026 كمرجع.
    """
    status = analysis_result.get('status')

    # التعامل مع حالة عدم وجود بيانات فوراً بدون تدخل الذكاء الاصطناعي
    if status == 'no_data':
        return "مدري والله ماعندي علم عن هالحي، البيانات ما تحضرني حالياً.. انشد ناس ثانين بيفيدونك أكثر."

    avg = analysis_result.get('avg_price_per_sqm', 0)
    count = analysis_result.get('deals_count', 0)
    trend = analysis_result.get('trend', 'غير معروف')
    change = analysis_result.get('change_percentage', 0)

    prompt = f"""
    أنت مستشار عقاري سعودي خبير وواقعي، تتحدث بلهجة عامية عفوية كأنك تسولف مع خويك في المجلس.

    **معلومة مهمة عن البيانات:** البيانات التي لديك تقف عند الربع الأول من عام 2026 (حتى شهر مارس). يجب أن توضح هذا للعميل بشفافية، وتخبره أن يستخدم هذا السعر كـ "مرجع" أو "مسطرة" يقيس عليها أسعار اليوم.

    بيانات السوق الموثقة لحي {district} في مدينة {city} (حتى مارس 2026):
    - اتجاه الحركة (الترند): {trend}
    - نسبة التغير المسجلة: {change}%
    - متوسط السعر: {avg:,.0f} ريال/م²
    - إجمالي الصفقات: {count} صفقة

    **قواعد الأسلوب والمصطلحات (مهم جداً):**
    1. ابدأ بترحيب عفوي مثل "هلا بك يا غالي" أو "شف طال عمرك".
    2. وضح أن هذه الأرقام هي قراءة للسوق حتى شهر مارس 2026.
    3. إذا كان السوق يشهد نزولاً غير جيد أو أرقاماً سلبية، استخدم كلمة **"ماش"** في سياق الحديث (بمعنى: الوضع لا يشجع ولا أنصحك به).
    4. إذا كان السوق متذبذباً، أو نسبة التغير بسيطة جداً (استقرار تام)، استخدم عبارة **"مو ذاك الزود"** (بمعنى: يمشي الحال وفيه استقرار، لكن فيه خيارات أفضل إذا تدور استثمار قوي).
    5. تجنب الجزم القطعي أو التهويل (لا تستخدم كلمات مثل: انهيار، مدحدر، طاير).
    6. في النهاية، انصحه بأن يمسك متوسط السعر المذكور كمعيار يتفاوض بناءً عليه اليوم.

    اكتب الرد الآن بلهجة سعودية طبيعية جداً:
    """

    try:
        response = model.generate_content(prompt)
        # تنظيف النص من علامات التنسيق الخاصة بـ Markdown عشان يكون كأنه رسالة واتساب طبيعية
        clean_text = response.text.replace('*', '').replace('#', '').strip()
        return clean_text
    except Exception as e:
        print(f"خطأ في جيميناي: {e}")
        return "والله يا غالي النظام معلق معي شوي، دقايق وارجع اسألني."


# --- دوال التليجرام ---

@bot.message_handler(func=lambda message: message.chat.id not in authenticated_users)
def check_password(message):
    if message.text.strip() == BOT_PASSWORD:
        authenticated_users.add(message.chat.id)
        bot.reply_to(message,
                     "✅ حياك الله، تم تسجيل الدخول.\nوش الحي اللي تدور فيه طال عمرك؟ (اكتب المدينة ثم الحي، مثال: الرياض الملقا)")
    else:
        bot.reply_to(message, "⛔️ البوت خاص ومحمي برقم سري.\nعطني الباسورد للدخول:")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.chat.id not in authenticated_users:
        bot.reply_to(message, "هلا بك! أرسل الباسورد الخاص بالبوت عشان أقدر أخدمك:")
    else:
        bot.reply_to(message, "هلا بك 🎯\nعطني اسم الحي اللي تدور فيه، مثال: (الرياض حطين)")


@bot.message_handler(func=lambda message: message.chat.id in authenticated_users)
def handle_district_query(message):
    text = message.text.strip().split()

    if len(text) < 2:
        bot.reply_to(message, "يا ليت تكتب اسم المدينة وبعدها الحي. مثال: الرياض النرجس")
        return

    city = text[0]
    district = " ".join(text[1:])

    msg = bot.reply_to(message, "أبشر، ثواني أقرأ لك الأرقام وأشاورك...")

    try:
        result = analyzer.analyze_district_trend(city, district)
        advice = get_gemini_advice(city, district, result)
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=advice)
    except Exception as e:
        print(f"حدث خطأ أثناء المعالجة: {e}")
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                              text="معليش، واجهت مشكلة فنية. جرب مرة ثانية بعد شوي.")


if __name__ == "__main__":
    print("✅ البوت جاهز ومحدث بلمسة بشرية! ينتظر الرسائل...")
    bot.infinity_polling()