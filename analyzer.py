import pandas as pd
import re
from data_handler import load_and_clean_datasets


def clean_arabic_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    return text.strip().lower()


class RealEstateAnalyzer:
    def __init__(self):
        print("⏳ جاري تهيئة المحلل العقاري...")
        self.datasets = load_and_clean_datasets()

        if self.datasets:
            self.df_2026 = self.datasets.get('sales_2026')
            self.df_2026['clean_city'] = self.df_2026['city'].apply(clean_arabic_text)
            self.df_2026['clean_district'] = self.df_2026['district'].apply(clean_arabic_text)
            if 'property_type' in self.df_2026.columns:
                self.df_2026['clean_property_type'] = self.df_2026['property_type'].apply(clean_arabic_text)
            print("✅ المحلل جاهز للعمل!")
        else:
            print("❌ فشل تحميل البيانات للمحلل.")

    def analyze_district_trend(self, city_name, district_name, property_type=None):
        if self.df_2026 is None:
            return {"error": "البيانات غير متوفرة."}

        clean_city_input = clean_arabic_text(city_name)
        clean_district_input = clean_arabic_text(district_name)

        # 1. فلترة المدينة والحي
        condition = (
                self.df_2026['clean_city'].str.contains(clean_city_input, na=False) &
                self.df_2026['clean_district'].str.contains(clean_district_input, na=False)
        )
        district_data = self.df_2026[condition].copy()
        print(f"\n🔍 [فحص 1] عدد الصفقات في {district_name} ({city_name}): {len(district_data)}")

        # طباعة أنواع العقارات الموجودة في هذا الحي عشان نعرف وش نكتب
        if not district_data.empty and 'property_type' in district_data.columns:
            print(f"🔍 [فحص أنواع العقارات الموجودة]:\n{district_data['property_type'].value_counts()}")

        # 2. فلترة نوع العقار
        if property_type and 'clean_property_type' in district_data.columns:
            clean_type_input = clean_arabic_text(property_type)
            district_data = district_data[district_data['clean_property_type'].str.contains(clean_type_input, na=False)]
            print(f"🔍 [فحص 2] عدد الصفقات بعد تحديد نوع العقار ({property_type}): {len(district_data)}")

        if district_data.empty:
            return {"status": "no_data", "message": "توقفت الفلترة هنا: لا يوجد بيانات بهذه المواصفات."}

        # 3. فحص التواريخ
        print(f"🔍 [فحص التواريخ قبل التنظيف]:\n{district_data['date'].head()}")
        district_data['date'] = pd.to_datetime(district_data['date'], errors='coerce')
        district_data = district_data.dropna(subset=['date'])
        print(f"🔍 [فحص 3] عدد الصفقات اللي تواريخها سليمة: {len(district_data)}")

        district_data = district_data[district_data['size'] > 0]

        if district_data.empty:
            return {"status": "no_data", "message": "توقفت الفلترة لأن التواريخ مفقودة أو المساحات صفر."}

        # حساب سعر المتر
        if 'price_per_sqm' not in district_data.columns or district_data['price_per_sqm'].isnull().any():
            district_data['price_per_sqm'] = district_data['price'] / district_data['size']

        district_data = district_data.sort_values(by='date')
        deals_count = len(district_data)
        current_avg_sqm = district_data['price_per_sqm'].mean()

        if deals_count < 3:
            return {"status": "low_data", "trend": "غير واضح", "message": "عدد الصفقات قليل جداً"}

        mid_point = deals_count // 2
        older_deals = district_data.iloc[:mid_point]
        newer_deals = district_data.iloc[mid_point:]

        avg_old_sqm = older_deals['price_per_sqm'].mean()
        avg_new_sqm = newer_deals['price_per_sqm'].mean()

        change_percentage = ((avg_new_sqm - avg_old_sqm) / avg_old_sqm) * 100

        if change_percentage > 3:
            trend = "صاعد"
        elif change_percentage < -3:
            trend = "نازل"
        else:
            trend = "مستقر"

        return {
            "status": "success",
            "trend": trend,
            "change_percentage": round(change_percentage, 1),
            "avg_price_per_sqm": round(current_avg_sqm, 0),
            "deals_count": deals_count
        }


if __name__ == "__main__":
    analyzer = RealEstateAnalyzer()
    print("-" * 40)
    # بنجرب نبحث عن الملقا بدون تحديد نوع العقار بالبداية عشان نشوف كل الأنواع
    result = analyzer.analyze_district_trend("الرياض", "الملقا")
    print("\nالنتيجة النهائية:")
    print(result)
    print("-" * 40)