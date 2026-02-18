def calculate_myntra_kuchipoo_payout_v2(
    mrp,
    discount,
    product_cost,
    brand,
    category,
    gender,
    apply_kuchipoo_royalty='No'
):
    GST_RATE = 0.18

    # 1️⃣ Selling Price
    selling_price = mrp - discount
    if selling_price <= 0:
        return {"Error": "Invalid Selling Price"}

    # 2️⃣ Taxable Calculation
    if selling_price >= 2500:
        divisor = 1.12
    else:
        divisor = 1.05

    taxable_value = selling_price / divisor

    # 3️⃣ Fixed Fee (New Structure)
    gt_charge = calculate_myntra_new_fixed_fee(brand, taxable_value)
    yk_fixed_fee = calculate_myntra_yk_fixed_fee(brand, taxable_value)

    total_fixed = gt_charge + yk_fixed_fee

    # 4️⃣ Seller Price (Commission Base)
    seller_price_for_commission = selling_price - gt_charge

    commission_rate = get_myntra_new_commission_rate(
        brand, category, gender, seller_price_for_commission
    )

    commission_base = seller_price_for_commission * commission_rate
    commission_gst = commission_base * GST_RATE
    final_commission = commission_base + commission_gst

    # 5️⃣ Royalty
    royalty_fee = calculate_myntra_new_royalty(
        brand,
        selling_price,
        apply_kuchipoo_royalty
    )

    # 6️⃣ Marketing Fee
    if brand == "KUCHIPOO":
        marketing_base = selling_price * 0.05
    elif brand in ["YK", "YK Disney", "YK Marvel"]:
        marketing_base = selling_price * 0.04
    else:
        marketing_base = 0.0

    marketing_gst = marketing_base * 0.18

    # 7️⃣ Platform Deduction
    total_platform_deduction = final_commission + total_fixed

    # 8️⃣ Settlement
    settled_amount = selling_price - total_platform_deduction

    # 9️⃣ Net Profit
    net_profit = (
        settled_amount
        - product_cost
        - royalty_fee
        - marketing_base
        - marketing_gst
    )

    return {
        "Brand": brand,
        "Selling Price": round(selling_price, 2),
        "Taxable Value": round(taxable_value, 2),
        "Fixed Fee (+GST)": round(total_fixed, 2),
        "Commission Rate": commission_rate,
        "Commission (+GST)": round(final_commission, 2),
        "Royalty": round(royalty_fee, 2),
        "Marketing (You Pay)": round(marketing_base + marketing_gst, 2),
        "Bank Settlement": round(settled_amount, 2),
        "Net Profit": round(net_profit, 2)
    }
