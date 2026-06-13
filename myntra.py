import pandas as pd
import streamlit as st
from io import BytesIO

FULL_TITLE = "Myntra E-commerce Calculator"
st.set_page_config(layout="wide", page_title=FULL_TITLE, page_icon="🛍️")

st.markdown("""
<style>
    .block-container {
        padding-top: 1.25rem; padding-bottom: 0.5rem; padding-left: 1rem;
        padding-right: 1rem; max-width: 1840px; margin-left: auto; margin-right: auto;
    }
    h1, h2, h3, h4, h5, h6 { margin-top: 0.5rem; margin-bottom: 0.25rem; }
    h1 { font-size: 2.25rem; line-height: 1.1; margin-top: 1.0rem; }
    hr { margin: 0.5rem 0 !important; }
    [data-testid="stMetric"] { padding-top: 0px; padding-bottom: 0px; }
    [data-testid="stMetricLabel"] { margin-bottom: -0.1rem; font-size: 0.8rem; }
    [data-testid="stMetricValue"] { font-size: 1.5rem; }
    .st-emotion-cache-12quz0q { gap: 0.75rem; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) {
        border-right: 1px solid rgba(255, 255, 255, 0.1); padding-right: 1rem;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) { padding-left: 1rem; }
</style>
""", unsafe_allow_html=True)


MYNTRA_COMMISSION_DATA = {
    "KUCHIPOO": {
        "Sweatshirts": {
            "Boys": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29},
            "Girls": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29}
        },
        "Clothing Set": {
            "Boys": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29},
            "Girls": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29}
        },
        "Tshirts": {
            "Boys": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29},
            "Girls": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29}
        },
        "Track Pants": {
            "Boys": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29},
            "Girls": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29}
        },
        "Shorts": {
            "Boys": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29},
            "Girls": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29}
        },
        "Dresses": {
            "Girls": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29}
        },
        "Sweaters": {
            "Boys": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29},
            "Girls": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29}
        },
        "Jeans": {
            "Boys": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29},
            "Girls": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29}
        },
        "Kurta Sets": {
            "Boys": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29},
            "Girls": {"0-200": 0.33, "200-300": 0.22, "300-400": 0.19, "400-500": 0.22, "500-800": 0.24, "800+": 0.29}
        }
    },
    "YK": {
        "Clothing Set": {
            "Boys": {"0-300": 0.05, "300-500": 0.05, "500-1000": 0.06, "1000-2000": 0.04, "2000+": 0.04},
            "Girls": {"0-300": 0.04, "300-500": 0.05, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.07}
        },
        "Dresses": {
            "Girls": {"0-300": 0.07, "300-500": 0.05, "500-1000": 0.04, "1000-2000": 0.00, "2000+": 0.00}
        },
        "Lounge Pants": { 
            "Boys": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.06},
            "Girls": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.06}
        },
        "Shorts": {
            "Boys": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.08},
            "Girls": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.08}
        },
        "Sweatshirts": {
            "Boys": {"0-300": 0.01, "300-500": 0.03, "500-1000": 0.07, "1000-2000": 0.07, "2000+": 0.09},
            "Girls": {"0-300": 0.01, "300-500": 0.03, "500-1000": 0.05, "1000-2000": 0.06, "2000+": 0.08}
        },
        "Track Pants": {
            "Boys": {"0-300": 0.08, "300-500": 0.08, "500-1000": 0.07, "1000-2000": 0.06, "2000+": 0.08},
            "Girls": {"0-300": 0.05, "300-500": 0.08, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.08}
        },
        "Tshirts": {
            "Boys": {"0-300": 0.10, "300-500": 0.10, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.08},
            "Girls": {"0-300": 0.10, "300-500": 0.10, "500-1000": 0.06, "1000-2000": 0.07, "2000+": 0.08}
        }
    },
    "YK Disney": {
        "Clothing Set": {
            "Boys": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.05, "1000-2000": 0.06, "2000+": 0.08},
            "Girls": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.05, "2000+": 0.08}
        },
        "Dresses": {
            "Girls": {"0-300": 0.08, "300-500": 0.08, "500-1000": 0.06, "1000-2000": 0.04, "2000+": 0.08}
        },
        "Lounge Pants": {
            "Boys": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.06},
            "Girls": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.06}
        },
        "Shorts": {
            "Boys": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.05, "2000+": 0.08},
            "Girls": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.05, "2000+": 0.08}
        },
        "Sweatshirts": {
            "Boys": {"0-300": 0.01, "300-500": 0.03, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.08},
            "Girls": {"0-3D": 0.01, "300-500": 0.03, "500-1000": 0.06, "1000-2000": 0.04, "2000+": 0.08}
        },
        "Track Pants": {
            "Boys": {"0-300": 0.08, "300-500": 0.08, "500-1000": 0.06, "1000-2000": 0.04, "2000+": 0.08},
            "Girls": {"0-300": 0.08, "300-500": 0.08, "500-1000": 0.05, "1000-2000": 0.05, "2000+": 0.08}
        },
        "Tshirts": {
            "Boys": {"0-300": 0.1, "300-500": 0.1, "500-1000": 0.06, "1000-2000": 0.05, "2000+": 0.08},
            "Girls": {"0-300": 0.1, "300-500": 0.1, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.08}
        }
    },
    "YK Marvel": {
        "Clothing Set": {
            "Boys": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.08}
        },
        "Lounge Pants": {
            "Boys": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.06}
        },
        "Shorts": {
            "Boys": {"0-300": 0.09, "300-500": 0.09, "500-1000": 0.06, "1000-2000": 0.03, "2000+": 0.08}
        },
        "Sweatshirts": {
            "Boys": {"0-300": 0.01, "300-500": 0.03, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.08}
        },
        "Track Pants": {
            "Boys": {"0-300": 0.08, "300-500": 0.08, "500-1000": 0.05, "1000-2000": 0.04, "2000+": 0.08}
        },
        "Tshirts": {
            "Boys": {"0-300": 0.1, "300-500": 0.1, "500-1000": 0.06, "1000-2000": 0.06, "2000+": 0.08}
        }
    }
}

def get_myntra_new_commission_rate(brand, category, gender, seller_price):
    try:
        brand_data = MYNTRA_COMMISSION_DATA.get(brand)
        if not brand_data: return 0.0
        
        category_data = brand_data.get(category)
        if not category_data: return 0.0
        
        gender_data = category_data.get(gender)
        if not gender_data: return 0.0
        
        if brand == "KUCHIPOO":
            if seller_price <= 200: return gender_data.get("0-200", 0.0)
            elif seller_price <= 300: return gender_data.get("200-300", 0.0)
            elif seller_price <= 400: return gender_data.get("300-400", 0.0)
            elif seller_price <= 500: return gender_data.get("400-500", 0.0)
            elif seller_price <= 800: return gender_data.get("500-800", 0.0)
            else: return gender_data.get("800+", 0.0)
        else: 
            if seller_price <= 300: return gender_data.get("0-300", 0.0)
            elif seller_price <= 500: return gender_data.get("300-500", 0.0)
            elif seller_price <= 1000: return gender_data.get("500-1000", 0.0)
            elif seller_price <= 2000: return gender_data.get("1000-2000", 0.0)
            else: return gender_data.get("2000+", 0.0)
            
    except Exception:
        return 0.0

def calculate_myntra_new_fixed_fee(brand, taxable_value_for_slab):
    base_fee = 0.0 
    
    if taxable_value_for_slab <= 500:
        base_fee = 50.0
    elif taxable_value_for_slab <= 1000:
        base_fee = 80.0
    elif taxable_value_for_slab <= 2000:
        base_fee = 145.0
    else: 
        base_fee = 175.0
    
    gst_on_fee = base_fee * 0.18
    final_fee = base_fee + gst_on_fee
            
    return final_fee 

def calculate_myntra_new_royalty(brand, sale_price, apply_kuchipoo_royalty_flag):
    royalty_rate = 0.0
    
    if brand == "YK":
        royalty_rate = 0.01 
    elif brand == "YK Disney":
        royalty_rate = 0.07 
    elif brand == "YK Marvel":
        royalty_rate = 0.07 
    elif brand == "KUCHIPOO" and apply_kuchipoo_royalty_flag == 'Yes':
        royalty_rate = 0.10 
        
    return sale_price * royalty_rate

def calculate_myntra_yk_fixed_fee(brand, taxable_value_for_slab):
    if brand not in ["YK", "YK Disney", "YK Marvel"]:
        return 0.0 

    base_fee = 0.0
    if taxable_value_for_slab <= 1000:
        base_fee = 27.0
    else: 
        base_fee = 45.0
    
    gst_on_fee = base_fee * 0.18
    final_fee = base_fee + gst_on_fee
            
    return final_fee

def calculate_taxable_amount_value(customer_paid_amount):
    if customer_paid_amount >= 2500:
        tax_rate = 0.12
        divisor = 1.12
    else:
        tax_rate = 0.05
        divisor = 1.05
    taxable_amount = customer_paid_amount / divisor
    return taxable_amount, tax_rate

def perform_calculations(mrp, discount, product_cost, 
                           myntra_brand=None, myntra_category=None, myntra_gender=None,
                           apply_kuchipoo_royalty='No',
                           yk_return_charges=0.0, yk_return_product_cost=0.0):
    
    sale_price = mrp - discount 
        
    if sale_price < 0:
        return (sale_price, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -99999999.0, 0.0, 0.0, 0.0, 0.0) 

    customer_paid_amount = sale_price 
    GST_RATE_FEES = 0.18 

    # --- COMMON TAX CALCULATION ---
    taxable_amount_value, invoice_tax_rate = calculate_taxable_amount_value(customer_paid_amount)
    tax_amount = customer_paid_amount - taxable_amount_value
    tds = taxable_amount_value * 0.001
    tcs = tax_amount * 0.10 

    # --- MYNTRA SPECIFIC FEES ---
    gt_charge = calculate_myntra_new_fixed_fee(myntra_brand, taxable_amount_value) 
    yk_fixed_fee = calculate_myntra_yk_fixed_fee(myntra_brand, taxable_amount_value) 

    seller_price = customer_paid_amount - gt_charge 
    
    commission_rate = get_myntra_new_commission_rate(myntra_brand, myntra_category, myntra_gender, seller_price) 
        
    commission_base = seller_price * commission_rate
    commission_tax = commission_base * GST_RATE_FEES
    final_commission = commission_base + commission_tax
    
    royalty_fee = calculate_myntra_new_royalty(myntra_brand, customer_paid_amount, apply_kuchipoo_royalty) 
    
    if myntra_brand == "KUCHIPOO":
        marketing_fee_base = customer_paid_amount * 0.05
    elif myntra_brand in ["YK", "YK Disney", "YK Marvel"]:
        marketing_fee_base = customer_paid_amount * 0.04
    else:
        marketing_fee_base = 0.0
        
    marketing_fee_gst = marketing_fee_base * 0.18 
    
    # --- Deductions & Settlement ---
    total_deductions = final_commission + gt_charge + yk_fixed_fee 
    settled_amount = customer_paid_amount - total_deductions - tds - tcs
    
    # --- Net Profit ---
    net_profit = settled_amount - product_cost - royalty_fee - marketing_fee_base - marketing_fee_gst
    
    if myntra_brand in ["YK", "YK Disney", "YK Marvel"]:
        net_profit = net_profit - yk_return_charges - yk_return_product_cost

    return (sale_price, gt_charge, customer_paid_amount, royalty_fee,
            marketing_fee_base, marketing_fee_gst,
            final_commission, 
            commission_rate, settled_amount, taxable_amount_value,
            net_profit, tds, tcs, invoice_tax_rate, yk_fixed_fee)

def find_discount_for_target_profit(mrp, target_profit, product_cost, 
                                    myntra_brand=None, myntra_category=None, myntra_gender=None,
                                    apply_kuchipoo_royalty='No',
                                    yk_return_charges=0.0, yk_return_product_cost=0.0):

    def get_net_profit(disc):
        results = perform_calculations(mrp, disc, product_cost,
                                       myntra_brand, myntra_category, myntra_gender,
                                       apply_kuchipoo_royalty,
                                       yk_return_charges, yk_return_product_cost)
        if results is None: return -9999.0
        return results[10]

    step_size = 5.0
    initial_profit = get_net_profit(0.0) 
    if initial_profit < target_profit:
        return None, initial_profit, 0.0 

    required_discount = 0.0
    while required_discount <= mrp:
        current_profit = get_net_profit(required_discount)
        if current_profit < target_profit:
            final_discount = max(0.0, required_discount - step_size)
            final_profit = get_net_profit(final_discount)
            discount_percent = (final_discount / mrp) * 100
            return final_discount, final_profit, discount_percent
        required_discount += step_size

    final_profit = get_net_profit(mrp)
    return mrp, final_profit, 100.0


def run_bulk_processing(df, mode, target_margin=0.0):
    
    results = []
    cols = df.columns
    
    sku_col_name = 'seller_sku_code' if 'seller_sku_code' in cols else 'sku_code' if 'sku_code' in cols else None
    mrp_col_name = 'product_mrp' if 'product_mrp' in cols else 'mrp' if 'mrp' in cols else 'product_mrp_' if 'product_mrp_' in cols else None
    cost_col_name = 'product_cost' if 'product_cost' in cols else 'cost_price' if 'cost_price' in cols else None
    selling_price_col_name = 'selling_price' if 'selling_price' in cols else None

    required_cols_check = [sku_col_name, mrp_col_name, cost_col_name]
    if mode == 'Check With Selling Price': 
        if not selling_price_col_name:
            st.error("File missing required column: 'selling_price' is needed for 'Check With Selling Price' mode.")
            return pd.DataFrame()
        required_cols_check.append(selling_price_col_name)

    if not all(required_cols_check):
        st.error(f"File missing required columns. Need SKU, MRP, and Cost. Check template downloads.")
        return pd.DataFrame()

    brand_col = 'myntra_brand' if 'myntra_brand' in cols else 'brand' if 'brand' in cols else None
    cat_col = 'myntra_article_type' if 'myntra_article_type' in cols else 'article_type' if 'article_type' in cols else None
    gen_col = 'myntra_gender' if 'myntra_gender' in cols else 'gender' if 'gender' in cols else None
    
    ret_charges_col = 'return_charges' if 'return_charges' in cols else None
    ret_cost_col = 'return_product_cost' if 'return_product_cost' in cols else None

    output_rows = []

    for row in df.itertuples():
        try:
            sku = str(getattr(row, sku_col_name))
            mrp = float(getattr(row, mrp_col_name))
            cost = float(getattr(row, cost_col_name))

            if mrp <= 0 or cost <= 0: continue 

            myntra_brand = getattr(row, brand_col) if brand_col and hasattr(row, brand_col) else None
            myntra_cat = getattr(row, cat_col) if cat_col and hasattr(row, cat_col) else None
            myntra_gen = getattr(row, gen_col) if gen_col and hasattr(row, gen_col) else None
            
            yk_ret_chg = float(getattr(row, ret_charges_col)) if ret_charges_col and hasattr(row, ret_charges_col) else 0.0
            yk_ret_cost = float(getattr(row, ret_cost_col)) if ret_cost_col and hasattr(row, ret_cost_col) else 0.0

            apply_kuchipoo_royalty = 'No'
            is_myntra_royalty_sku = sku.startswith("DKUC") or sku.startswith("MKUC")
            if myntra_brand == 'KUCHIPOO' and is_myntra_royalty_sku:
                apply_kuchipoo_royalty = 'Yes'
            
            output_data = {
                "SKU": sku,
                "MRP": mrp,
                "Cost_Price": cost,
            }

            if mode == 'Check With Selling Price':
                selling_price = float(getattr(row, selling_price_col_name))
                discount_amount = mrp - selling_price
                
                (sale_price, gt_charge, customer_paid_amount, royalty_fee,
                 marketing_fee_base, marketing_fee_gst, final_commission,
                 commission_rate, settled_amount, taxable_amount_value,
                 net_profit, tds, tcs, invoice_tax_rate, yk_fixed_fee 
                ) = perform_calculations(
                    mrp, discount_amount, cost,
                    myntra_brand, myntra_cat, myntra_gen, apply_kuchipoo_royalty,
                    yk_ret_chg, yk_ret_cost
                )
                
                output_data.update({
                    "Selling_Price": selling_price,
                    "Taxable_Amount": taxable_amount_value,
                    "Commission_(Inc_GST)": final_commission,
                    "Fixed_Fee_(Inc_GST)": gt_charge,
                    "YK_Fixed_Fee_(Inc_GST)": yk_fixed_fee,
                    "Total_Platform_Deductions": final_commission + gt_charge + yk_fixed_fee,
                    "TDS": tds,
                    "TCS": tcs,
                    "Bank_Settlement_Amount": settled_amount,
                    "Royalty_You_Pay": royalty_fee,
                    "Marketing_Fee_Base": marketing_fee_base,
                    "Marketing_Fee_GST": marketing_fee_gst,
                    "Marketing_Total_You_Pay": marketing_fee_base + marketing_fee_gst,
                    "Return_Charges": yk_ret_chg,
                    "Return_Cost_Loss": yk_ret_cost,
                    "Net_Profit_In_Hand": net_profit
                })

            else: 
                discount_amount, final_profit, discount_percent = find_discount_for_target_profit(
                    mrp, target_margin, cost,
                    myntra_brand, myntra_cat, myntra_gen, apply_kuchipoo_royalty,
                    yk_ret_chg, yk_ret_cost
                )
                
                selling_price_req = (mrp - discount_amount) if discount_amount is not None else "N/A"
                
                taxable_amt = "N/A"
                comm_inc_gst = "N/A"
                fixed_inc_gst = "N/A"
                yk_fixed_inc_gst = "N/A"
                total_plat_deduct = "N/A"
                tds_val = "N/A"
                tcs_val = "N/A"
                bank_settlement_amt = "N/A"
                royalty_val = "N/A"
                mkt_base = "N/A"
                mkt_gst = "N/A"
                marketing_total_pay = "N/A"

                if discount_amount is not None:
                    (sale_price, gt_charge, customer_paid_amount, royalty_fee,
                     marketing_fee_base, marketing_fee_gst, final_commission,
                     commission_rate, settled_amount, taxable_amount_value,
                     net_profit, tds, tcs, invoice_tax_rate, yk_fixed_fee 
                    ) = perform_calculations(
                        mrp, discount_amount, cost,
                        myntra_brand, myntra_cat, myntra_gen, apply_kuchipoo_royalty,
                        yk_ret_chg, yk_ret_cost
                    )
                    taxable_amt = taxable_amount_value
                    comm_inc_gst = final_commission
                    fixed_inc_gst = gt_charge
                    yk_fixed_inc_gst = yk_fixed_fee
                    total_plat_deduct = final_commission + gt_charge + yk_fixed_fee
                    tds_val = tds
                    tcs_val = tcs
                    bank_settlement_amt = settled_amount
                    royalty_val = royalty_fee
                    mkt_base = marketing_fee_base
                    mkt_gst = marketing_fee_gst
                    marketing_total_pay = marketing_fee_base + marketing_fee_gst

                output_data.update({
                    "Target_Margin": target_margin,
                    "Required_Selling_Price": selling_price_req,
                    "Taxable_Amount": taxable_amt,
                    "Commission_(Inc_GST)": comm_inc_gst,
                    "Fixed_Fee_(Inc_GST)": fixed_inc_gst,
                    "YK_Fixed_Fee_(Inc_GST)": yk_fixed_inc_gst,
                    "Total_Platform_Deductions": total_plat_deduct,
                    "TDS": tds_val,
                    "TCS": tcs_val,
                    "Bank_Settlement_Amount": bank_settlement_amt,
                    "Royalty_You_Pay": royalty_val,
                    "Marketing_Fee_Base": mkt_base,
                    "Marketing_Fee_GST": mkt_gst,
                    "Marketing_Total_You_Pay": marketing_total_pay,
                    "Return_Charges": yk_ret_chg,
                    "Return_Cost_Loss": yk_ret_cost,
                    "Projected_Net_Profit": final_profit if final_profit is not None else "N/A"
                })

            output_rows.append(output_data)

        except Exception as e:
            continue
            
    return pd.DataFrame(output_rows)


@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# ==============================================================================
# --- MAIN APP STRUCTURE ---
# ==============================================================================

st.title("🛍️ " + FULL_TITLE)
st.markdown("###### **1. Select Mode**")
main_mode = st.radio("Select Mode", ("Single Product Calculation", "Bulk Calculation"), horizontal=True, label_visibility="collapsed")

st.markdown("###### **2. Upload SKU File (CSV or XLSX)**")

sku_col_1, sku_col_2 = st.columns([3, 1])

with sku_col_1:
    sku_file = st.file_uploader("Upload your Myntra SKU file:", type=['csv', 'xlsx'])

with sku_col_2:
    if 'sku_df' in st.session_state:
        def clear_sku_data():
            st.session_state.pop('sku_df', None)
            st.session_state.pop('sku_select_key', None)
            
            keys_to_clear = ['myntra_brand_v3', 'myntra_cat_v3', 'myntra_gen_v3', 'new_mrp', 'single_cost']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]

        st.button("Clear SKU Data", on_click=clear_sku_data, use_container_width=True)

if sku_file is not None and 'sku_df' not in st.session_state:
    try:
        if sku_file.name.endswith('.xlsx'):
            df = pd.read_excel(sku_file, dtype=str, engine='openpyxl')
        else:
            df = pd.read_csv(sku_file, encoding='utf-8-sig', dtype=str)
        
        df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
        st.session_state.sku_df = df
        st.success(f"Successfully loaded {len(df)} SKUs.")
    except Exception as e:
        st.error(f"Error loading SKU file: {e}")

st.markdown("**Download Templates (CSV):**")
with st.expander("Show Templates"):
    template_mode = st.radio("Template format for:", ("Check With Selling Price", "Check With Cost Price"), horizontal=True)
    
    if template_mode == "Check With Selling Price":
        myntra_template_csv = "seller_sku_code,product_mrp,product_cost,selling_price,brand,article_type,gender,style_id,style_name,return_charges,return_product_cost\nDKUC-TEST-001,1999,500,1499,KUCHIPOO,Tshirts,Boys,123456,Test Style,0,0\nYK-TEST-002,1999,600,1299,YK,Tshirts,Boys,123457,YK Style,45,150\n"
    else:
        myntra_template_csv = "seller_sku_code,product_mrp,product_cost,brand,article_type,gender,style_id,style_name,return_charges,return_product_cost\nDKUC-TEST-001,1999,500,KUCHIPOO,Tshirts,Boys,123456,Test Style,0,0\nYK-TEST-002,1999,600,YK,Tshirts,Boys,123457,YK Style,45,150\n"

    st.download_button("Myntra Template", data=myntra_template_csv, file_name="myntra_template.csv", mime="text/csv")

st.divider()

if main_mode == "Single Product Calculation":

    st.markdown("###### **3. Select Calculation Mode**")
    single_calc_mode = st.radio(
        "Select Calculation Mode:", 
        ('Check With Selling Price', 'Check With Cost Price'),
        index=0, label_visibility="collapsed", horizontal=True
    )
    st.markdown("---")

    def lookup_sku():
        sku = st.session_state.get('sku_select_key', '').strip() 
        if not sku or sku == "Select SKU...": return

        if 'sku_df' in st.session_state:
            sku_df = st.session_state.sku_df
            cols = sku_df.columns
            sku_col_name = 'seller_sku_code' if 'seller_sku_code' in cols else 'sku_code'
            mrp_col_name = 'product_mrp' if 'product_mrp' in cols else 'mrp'
            cost_col_name = 'product_cost' if 'product_cost' in cols else 'cost_price'
            
            result = sku_df[sku_df[sku_col_name].astype(str).str.lower() == sku.lower()]
            
            if not result.empty:
                row = result.iloc[0]
                try: st.session_state.new_mrp = float(row[mrp_col_name])
                except: pass
                try: st.session_state.single_cost = float(row[cost_col_name])
                except: pass

                brand_col = 'myntra_brand' if 'myntra_brand' in cols else 'brand' 
                cat_col = 'myntra_article_type' if 'myntra_article_type' in cols else 'article_type'
                gen_col = 'myntra_gender' if 'myntra_gender' in cols else 'gender'
                if brand_col in row: st.session_state.myntra_brand_v3 = row[brand_col]
                if cat_col in row: st.session_state.myntra_cat_v3 = row[cat_col]
                if gen_col in row: st.session_state.myntra_gen_v3 = row[gen_col]

    if 'sku_df' in st.session_state:
        sku_df = st.session_state.sku_df 
        cols = sku_df.columns
        sku_col_name = 'seller_sku_code' if 'seller_sku_code' in cols else 'sku_code'
        
        if sku_col_name:
            sku_options = ["Select SKU..."] + sorted(st.session_state.sku_df[sku_col_name].dropna().unique().tolist())
            st.selectbox("**Fetch by SKU:**", options=sku_options, key="sku_select_key", on_change=lookup_sku)

    st.markdown("###### **4. Configuration Settings**")

    yk_return_charges = 0.0
    yk_return_product_cost = 0.0

    col_brand, col_cat, col_gen = st.columns(3)
    brand_options = list(MYNTRA_COMMISSION_DATA.keys())
    myntra_new_brand = col_brand.selectbox("Select Brand:", brand_options, key="myntra_brand_v3")
    
    try:
        category_options = list(MYNTRA_COMMISSION_DATA[myntra_new_brand].keys())
        myntra_new_category = col_cat.selectbox("Select Category:", category_options, key="myntra_cat_v3")
    except KeyError:
        category_options = []
        myntra_new_category = col_cat.selectbox("Select Category:", category_options, index=0, key="myntra_cat_v3")
    
    try:
        gender_options = list(MYNTRA_COMMISSION_DATA[myntra_new_brand][myntra_new_category].keys())
        myntra_new_gender = col_gen.selectbox("Select Gender:", gender_options, key="myntra_gen_v3")
    except KeyError:
            gender_options = []
            myntra_new_gender = col_gen.selectbox("Select Gender:", gender_options, index=0, key="myntra_gen_v3")
            
    if myntra_new_brand in ["YK", "YK Disney", "YK Marvel"]:
        st.markdown("**YK Brands Return Deductions (Optional)**")
        col_ret1, col_ret2 = st.columns(2)
        yk_return_charges = col_ret1.number_input("Average Return Logistics Charge (₹)", value=0.0, min_value=0.0)
        yk_return_product_cost = col_ret2.number_input("Average Return Product Loss (₹)", value=0.0, min_value=0.0)

    col_cost, col_target = st.columns(2)
    product_cost = col_cost.number_input("Product Cost (₹)", min_value=0.0, value=1000.0, key="single_cost")
    
    product_margin_target_rs = col_target.number_input("Target Net Profit (₹)", min_value=0.0, value=200.0, key="single_target", help="Net Profit you want in hand AFTER paying Royalty")
    
    st.divider()

    col_mrp_in, col_price_in = st.columns(2)
    new_mrp = col_mrp_in.number_input("Product MRP (₹)", min_value=1.0, value=2500.0, key="new_mrp")

    new_discount = 0.0

    if single_calc_mode == 'Check With Selling Price':
        new_discount = col_price_in.number_input("Discount Amount (₹)", value=500.0)

    st.divider()

    if new_mrp > 0 and product_cost > 0:
        
        apply_kuchipoo_royalty = 'No' 
        
        if 'sku_df' in st.session_state:
            selected_sku = st.session_state.get('sku_select_key', '').strip()
            is_myntra_royalty_sku = selected_sku and (selected_sku.startswith("DKUC") or selected_sku.startswith("MKUC"))
            if myntra_new_brand == 'KUCHIPOO' and is_myntra_royalty_sku:
                apply_kuchipoo_royalty = 'Yes'
                st.success(f"Royalty Active: 10% (SKU: {selected_sku})")

        # --- PERFORM CALCULATION ---
        if single_calc_mode == 'Check With Cost Price':
            calculated_discount, initial_max_profit, calculated_discount_percent = find_discount_for_target_profit(
                new_mrp, product_margin_target_rs, product_cost,
                myntra_new_brand, myntra_new_category, myntra_new_gender, apply_kuchipoo_royalty, 
                yk_return_charges, yk_return_product_cost
            )
            
            if calculated_discount is None:
                st.error(f"Cannot achieve Target Profit. Max possible profit at MRP is ₹ {initial_max_profit:,.2f}.")
                st.stop()
                
            new_discount = calculated_discount

        (sale_price, gt_charge, customer_paid_amount, royalty_fee,
         marketing_fee_base, marketing_fee_gst, final_commission,
         commission_rate, settled_amount, taxable_amount_value,
         net_profit, tds, tcs, invoice_tax_rate, yk_fixed_fee 
         ) = perform_calculations(
             new_mrp, new_discount, product_cost, 
             myntra_new_brand, myntra_new_category, myntra_new_gender, apply_kuchipoo_royalty, 
             yk_return_charges, yk_return_product_cost 
         )

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("### 1. Invoice & Sales")
            st.metric("Selling Price", f"₹ {sale_price:,.2f}")
            st.metric("Discount", f"₹ {new_discount:,.2f}")
            
            st.markdown("### 2. Platform Deductions")
            c1, c2 = st.columns(2)
            c1.metric("Commission (+GST)", f"₹ {final_commission:,.2f}")
            c2.metric("Fixed/Logistics (+GST)", f"₹ {gt_charge + yk_fixed_fee:,.2f}")

            total_deductions_display = final_commission + gt_charge + yk_fixed_fee 
            st.info(f"Total Platform Deductions: ₹ {total_deductions_display:,.2f}")

        with col_right:
            st.markdown("### 3. Settlement & Profit")
            
            st.metric("🏦 Bank Settlement", f"₹ {settled_amount:,.2f}")
            
            st.markdown("---")
            st.write("**Your Expenses after Settlement:**")
            ex1, ex2 = st.columns(2)
            ex1.metric("Product Cost", f"₹ {product_cost:,.2f}")
            ex2.metric("Royalty (You Pay)", f"₹ {royalty_fee:,.2f}", delta="Pay Externally", delta_color="inverse")
            
            ex3, ex4 = st.columns(2)
            ex3.metric("Marketing (You Pay)", f"₹ {marketing_fee_base:,.2f}", delta="Pay Externally", delta_color="inverse")
            ex4.metric("Mrkt GST (18%)", f"₹ {marketing_fee_gst:,.2f}", delta="Pay Externally", delta_color="inverse")
            
            if myntra_new_brand in ["YK", "YK Disney", "YK Marvel"] and (yk_return_charges > 0 or yk_return_product_cost > 0):
                ex5, ex6 = st.columns(2)
                ex5.metric("Return Logistics", f"₹ {yk_return_charges:,.2f}", delta="Deducted", delta_color="inverse")
                ex6.metric("Return Product Loss", f"₹ {yk_return_product_cost:,.2f}", delta="Deducted", delta_color="inverse")

            st.markdown("---")
            st.metric("💰 NET PROFIT (In Hand)", f"₹ {net_profit:,.2f}", delta=f"Target: ₹ {product_margin_target_rs:,.2f}")

elif main_mode == "Bulk Calculation":
    
    st.markdown("###### **3. Configure Bulk Calculation**")
    
    bulk_calc_mode = st.radio(
        "Select Calculation Mode", 
        ('Check With Selling Price', 'Check With Cost Price'),
        index=0, 
        horizontal=True,
        key="bulk_calc_mode_selector"
    )

    st.markdown("---")

    bulk_target_margin = 0.0

    if bulk_calc_mode == 'Check With Cost Price':
        bulk_target_margin = st.number_input("Target Margin Amount (₹) (per SKU)", min_value=0.0, value=100.0, step=10.0)

    st.info("Note: For Bulk Return calculations on YK Brands, include 'return_charges' and 'return_product_cost' columns in your CSV.")

    st.divider()

    if st.button("Run Bulk Calculation", use_container_width=True, type="primary"):
        if 'sku_df' not in st.session_state:
            st.error("Please upload an SKU file first.")
        else:
            with st.spinner("Processing..."):
                df_results = run_bulk_processing(
                    st.session_state.sku_df,
                    bulk_calc_mode,
                    target_margin=bulk_target_margin
                )
            
            if not df_results.empty:
                st.markdown("###### **4. Calculation Results**")
                st.dataframe(df_results.style.format(precision=2))
                csv_data = convert_df_to_csv(df_results)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv_data,
                    file_name=f"myntra_bulk_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )
