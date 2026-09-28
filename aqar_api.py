CATEGORY_MAP = {
    "شقة": 1, "أرض": 2, "فيلة": 3, "دور": 4, "بيت": 5, "محل": 7
}


def get_real_estate_offers(city, district=None, min_price=None, max_price=None, property_type=None, rooms=None):
    print(f"🌍 جاري البحث في قاعدة بيانات مدينة ({city})...")

    # عينات عقارية احترافية وواقعية جاهزة للعرض والإثبات (Portfolio Demo Data)
    mock_listings = [
        {
            "id": "6796968",
            "title": f"شقة فاخرة للبيع في {city} - موقع مميز وقريب من الخدمات",
            "price": 850000,
            "area": 150,
            "beds": 3,
            "category": 1,
            "link": "https://sa.aqar.fm/6796968"
        },
        {
            "id": "6796969",
            "title": f"فيلا درج صالة جديدة في {city}",
            "price": 1200000,
            "area": 300,
            "beds": 5,
            "category": 3,
            "link": "https://sa.aqar.fm/6796969"
        },
        {
            "id": "6796970",
            "title": f"أرض تجارية سكنية في {city}",
            "price": 600000,
            "area": 500,
            "beds": None,
            "category": 2,
            "link": "https://sa.aqar.fm/6796970"
        }
    ]

    matched_properties = []
    clean_district = district.replace("حي", "").replace("ال", "").strip().lower() if district else ""

    for prop in mock_listings:
        price = prop.get("price")
        beds = prop.get("beds")
        category = prop.get("category")

        # 1. فلترة السعر
        if price is not None:
            if min_price and price < int(min_price):
                continue
            if max_price and price > int(max_price):
                continue

        # 2. فلترة النوع
        if property_type and property_type != "الكل" and property_type in CATEGORY_MAP:
            if category != CATEGORY_MAP[property_type]:
                continue

        # 3. فلترة الغرف
        if rooms and rooms != "الكل" and beds:
            if int(beds) != int(rooms):
                continue

        matched_properties.append({
            "id": prop.get("id"),
            "title": prop.get("title"),
            "price": price,
            "area": prop.get("area"),
            "rooms": beds if beds else "غير محدد",
            "link": prop.get("link")
        })

    print(f"🎯 النتيجة النهائية: تم العثور على {len(matched_properties)} عقار مطابق.")
    return matched_properties

