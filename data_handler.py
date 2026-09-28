import pandas as pd


def load_and_clean_datasets():
    print("⏳ جاري تحميل وتنظيف قواعد البيانات...")
    try:
        df_aqar = pd.read_csv('data/SA_Aqar.csv')
        df_rent = pd.read_excel('data/daily_rent.xlsx')

        df_2025 = pd.read_csv('data/riyadh_2025.csv')
        df_2026 = pd.read_csv('data/riyadh_2026.csv')
        df_moj = pd.read_csv('data/moj_sales_riyadh_2026.csv')

        df_top = pd.read_csv('data/riyadh_top_districts_2026.csv')
        df_summary = pd.read_csv('data/riyadh_region_summary_2026.csv')

        def standardize_columns(df):
            rename_dict = {
                'المدينة': 'city',
                'الحي': 'district',
                'السعر': 'price',
                'المساحة': 'size',
                'سعر المتر': 'price_per_sqm',
                'سعر_المتر': 'price_per_sqm',
                'تصنيف العقار': 'property_type',
                'تصنيف_العقار': 'property_type',
                'تاريخ الصفقة ميلادي': 'date',
                'الرقم المرجعي للصفقة': 'deal_id',
                'الرقم المرجعي للعقار': 'property_id',
                'إجمالي المساحة': 'total_size',
                'إجمالي_المساحة': 'total_size',
                'متوسط المساحة': 'avg_size',
                'متوسط_المساحة': 'avg_size',
                'إجمالي القيمة': 'total_value',
                'إجمالي_القيمة': 'total_value',
                'متوسط السعر': 'avg_price',
                'متوسط_السعر': 'avg_price',
                'متوسط المتر': 'avg_price_per_sqm',
                'متوسط_المتر': 'avg_price_per_sqm',
                'عدد الصفقات': 'deals_count',
                'عدد_الصفقات': 'deals_count',
                'ادنى سعر': 'min_price',
                'ادنى_سعر': 'min_price',
                'أدنى_سعر': 'min_price',
                'اعلى سعر': 'max_price',
                'اعلى_سعر': 'max_price',
                'أعلى_سعر': 'max_price'
            }

            df.rename(columns=lambda x: str(x).strip(), inplace=True)
            df.rename(columns=rename_dict, inplace=True)

            if 'district' in df.columns:
                df['district'] = df['district'].astype(str).str.strip()
            if 'city' in df.columns:
                df['city'] = df['city'].astype(str).str.strip()

            return df

        df_2025 = standardize_columns(df_2025)
        df_2026 = standardize_columns(df_2026)
        df_moj = standardize_columns(df_moj)
        df_top = standardize_columns(df_top)
        df_summary = standardize_columns(df_summary)

        print("✅ تم تحميل وتنظيف البيانات وتوحيد أسماء الأعمدة لجميع الملفات بنجاح!\n")

        print("📋 أعمدة صفقات 2026 بعد التوحيد:")
        print(list(df_2026.columns))

        print("\n📋 أعمدة أكثر الأحياء مبيعاً بعد التوحيد:")
        print(list(df_top.columns))

        return {
            'aqar': df_aqar,
            'rent': df_rent,
            'sales_2025': df_2025,
            'sales_2026': df_2026,
            'moj_2026': df_moj,
            'top_districts': df_top,
            'region_summary': df_summary
        }

    except Exception as e:
        print(f"❌ حدث خطأ أثناء المعالجة: {e}")
        return None


if __name__ == "__main__":
    datasets = load_and_clean_datasets()