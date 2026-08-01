# دليل تشغيل النشر التلقائي على انستغرام (مجاني بالكامل)

هذا الدليل يشرح خطوة بخطوة كيف تفعّل النظام. خذ وقتك، كل خطوة مرة وحدة بس.

---

## الخطوة 1: إنشاء حساب GitHub ورفع الملفات

1. سوي حساب مجاني على github.com (إذا ما عندك)
2. أنشئ **مستودع (Repository) جديد**، خليه **Public**، وسمّه مثلاً `aqwal-ahlulbayt`
3. ارفع كل الملفات اللي بالمجلد المرفق (posts/، quotes.csv، post_instagram.py، .github/) لنفس المستودع
   - أسهل طريقة: اسحب المجلد كامل لصفحة المستودع بالمتصفح (Add file → Upload files)

---

## الخطوة 2: تفعيل GitHub Pages (لعرض الصور برابط عام)

1. بالمستودع، روح لـ **Settings → Pages**
2. تحت "Build and deployment" اختر **Deploy from a branch**
3. اختر Branch: `main` والمجلد `/ (root)`
4. احفظ. بعد دقيقة أو دقيقتين رح يعطيك رابط شكله:
   `https://اسم_المستخدم.github.io/aqwal-ahlulbayt`
5. احتفظ بهذا الرابط، رح تحتاجه بالخطوة 5

---

## الخطوة 3: ربط حساب انستا بتطبيق مطور (Facebook Developer App)

1. روح لـ developers.facebook.com وسجل دخول بنفس حساب الفيسبوك المربوط بصفحتك
2. My Apps → Create App → اختر نوع "Business"
3. من قائمة المنتجات أضف: **Instagram Graph API**
4. من صفحة "Graph API Explorer" (موجودة بنفس الموقع):
   - اختر التطبيق اللي سويته
   - اطلب صلاحيات: `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`
   - ولّد **Access Token** مؤقت

---

## الخطوة 4: تحويل التوكن إلى توكن طويل الأمد + جلب رقم حسابك

1. بـGraph API Explorer، نفذ هذا الطلب عشان تجيب صفحاتك:
   `GET /me/accounts`
   → انسخ `id` تبع صفحة الفيسبوك المربوطة بانستا
2. نفذ:
   `GET /{page-id}?fields=instagram_business_account`
   → هذا يعطيك **IG_USER_ID** (رقم حساب انستا Business)
3. لتحويل التوكن لتوكن طويل الأمد (يدوم ~60 يوم ويتجدد):
   `GET /oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-token}`
   → هذا هو **IG_ACCESS_TOKEN**

> ⚠️ التوكن الطويل ينتهي كل ~60 يوم وتحتاج تجدده يدوياً بنفس الطريقة، أو تربط تجديد تلقائي لاحقاً إذا حبيت.

---

## الخطوة 5: إضافة الأسرار (Secrets) والمتغيرات بالمستودع

بالمستودع على GitHub: **Settings → Secrets and variables → Actions**

**تبويب Secrets** (أضف Secret جديد لكل وحدة):
| الاسم | القيمة |
|---|---|
| `IG_USER_ID` | الرقم اللي جبته بالخطوة 4 |
| `IG_ACCESS_TOKEN` | التوكن الطويل اللي جبته بالخطوة 4 |

**تبويب Variables** (أضف Variable جديد):
| الاسم | القيمة |
|---|---|
| `GH_PAGES_BASE` | رابط GitHub Pages اللي جبته بالخطوة 2 (بدون / بالنهاية) |

---

## الخطوة 6: التجربة والتشغيل

1. روح لتبويب **Actions** بالمستودع
2. اختر "نشر يومي لانستغرام" من القائمة اليسرى
3. اضغط **Run workflow** عشان تجربه يدوياً أول مرة
4. لو نجح، رح تلاقي أول قول انشر على حسابك 🎉
5. من الآن وطالع، رح ينشر تلقائياً **3 مرات باليوم** بدون أي تدخل منك، ويدور على 30 يوم من جديد كل شهر

---

## إذا صار خطأ

- روح لتبويب Actions → اضغط على أي تشغيل فشل → اقرأ رسالة الخطأ (غالباً تكون مشكلة بالتوكن أو الصلاحيات)
- أكثر خطأ شائع: التوكن ما عنده صلاحية `instagram_content_publish`، أو الحساب مو Business/Creator مربوط بصفحة صح

أي خطوة تعلق فيها، ارجعلي واذكرلي رسالة الخطأ بالضبط وأساعدك.
