# calculator_app.py (3.0版本 - 网页版)
import streamlit as st
import math

# --- 定义基础信息和计算逻辑 (这些和之前一样) ---
GRANULE_STRENGTH_MG = 15
CAPSULE_STRENGTH_MG = 75
EXAMPLE_VOLUME_ML = 50

# 把核心计算逻辑封装成一个函数，这样更整洁
def get_dosage_instructions(weight_kg):
    # 1. 确定mg剂量
    dosage_mg = 0
    if weight_kg <= 15:
        dosage_mg = 30
    elif 15 < weight_kg <= 23:
        dosage_mg = 45
    elif 23 < weight_kg <= 40:
        dosage_mg = 60
    else:
        dosage_mg = 75

    # 2. 生成颗粒指导
    needed_granules = dosage_mg / GRANULE_STRENGTH_MG
    sachets_to_dissolve = math.ceil(needed_granules)
    total_granule_mg = sachets_to_dissolve * GRANULE_STRENGTH_MG
    granule_percent = (dosage_mg / total_granule_mg) * 100
    granule_ml = EXAMPLE_VOLUME_ML * (granule_percent / 100)

    # 3. 生成胶囊指导
    capsule_percent = (dosage_mg / CAPSULE_STRENGTH_MG) * 100
    capsule_ml = EXAMPLE_VOLUME_ML * (capsule_percent / 100)

    return {
        "dosage_mg": dosage_mg,
        "sachets_to_dissolve": sachets_to_dissolve,
        "granule_percent": granule_percent,
        "granule_ml": granule_ml,
        "capsule_percent": capsule_percent,
        "capsule_ml": capsule_ml
    }

# --- Streamlit 网页界面部分 ---
st.title("奥司他韦剂量计算器 💊")
st.caption("适用范围：1岁及以上儿童")

# st.number_input 创建一个网页上的数字输入框，替代了之前的 input()
weight_kg = st.number_input("请输入儿童体重 (kg):", min_value=0.1, step=0.1, format="%.1f")

# st.button 创建一个网页上的按钮
if st.button("开始计算"):
    if weight_kg:
        # 调用函数进行计算
        results = get_dosage_instructions(weight_kg)

        # st.success/info/write/markdown 在网页上显示格式化的结果
        st.success(f"对于体重为 {weight_kg}kg 的儿童，推荐单次剂量为: {results['dosage_mg']}mg，每日2次。")

        st.markdown("---")

        st.info("方案一：使用可威® 颗粒 (15mg/包)")
        st.write(f"建议：每日2次，每次冲泡 **{results['sachets_to_dissolve']}** 包颗粒，")
        st.write(f"取冲泡后液体总量的 **{results['granule_percent']:.0f}%** 饮用，其余丢弃。")
        st.write(f"↳ 例如：如果用 {EXAMPLE_VOLUME_ML}ml 水冲泡，那就喝 **{results['granule_ml']:.1f}ml**。")

        st.markdown("---")

        st.info("方案二：使用达菲® 胶囊 (75mg/粒)")
        if results['dosage_mg'] > CAPSULE_STRENGTH_MG:
             st.write("剂量超过单粒胶囊，请遵医嘱服用或使用颗粒剂。")
        else:
            st.write(f"建议：每日2次，每次冲泡 **1** 粒胶囊，")
            st.write(f"取冲泡后液体总量的 **{results['capsule_percent']:.0f}%** 饮用，其余丢弃。")
            st.write(f"↳ 例如：如果用 {EXAMPLE_VOLUME_ML}ml 水冲泡，那就喝 **{results['capsule_ml']:.1f}ml**。")

        st.markdown("---")
        st.warning("**重要提示**：本计算器为演示原型，计算结果不能替代执业医师、药师的当面诊断和处方，请务必在医生指导下用药。")
