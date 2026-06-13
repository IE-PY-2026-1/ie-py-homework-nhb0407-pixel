# =========================================================
# [Resell-Master V3.0] 굿즈 시세 분석 + 다중 굿즈 + 파일 저장
# 작성자: 남현빈
# 핵심 기능: 딕셔너리 기반 다중 굿즈 관리, 파일 입출력,
#            이벤트 계수, 가격 예측, 추천 판매가, 구매 추천 정렬
# =========================================================

# ---------------------------------------------------------
# [함수 정의 ①] get_trend(current, previous)
# ---------------------------------------------------------
def get_trend(current, previous):
    rate = (current - previous) / previous * 100
    if rate > 0:
        return rate, "📈 상승"
    elif rate < 0:
        return rate, "📉 하락"
    else:
        return rate, "➡️  보합"

# ---------------------------------------------------------
# [함수 정의 ②] get_timing(latest, min_price, avg_price)
# ---------------------------------------------------------
def get_timing(latest, min_price, avg_price):
    ratio = (latest / avg_price) * 100
    if latest <= min_price:
        return "🟢 역대 최저가! 최적 매수 타이밍!", 100
    elif ratio <= 90:
        return "🟡 평균가보다 저렴 — 매수 고려", 75
    elif ratio <= 105:
        return "🟠 평균가 근처 — 조금 더 지켜보세요", 50
    else:
        return "🔴 평균가보다 높음 — 매수 비추천", 25

# ---------------------------------------------------------
# [함수 정의 ③] get_sell_price(avg, max_price)
# 추천 판매가 = 평균가와 최고가의 중간값 기반
# ---------------------------------------------------------
def get_sell_price(avg, max_price):
    recommend = (avg + max_price) / 2
    return recommend

# ---------------------------------------------------------
# [함수 정의 ④] predict_price(prices, n_months)
# 선형 추세로 n개월 뒤 가격 예측
# ---------------------------------------------------------
def predict_price(prices, n_months):
    if len(prices) < 2:
        return prices[-1]
    # 전체 구간 평균 변화량 계산
    total_change = prices[len(prices)-1] - prices[0]
    avg_change   = total_change / (len(prices) - 1)
    predicted    = prices[len(prices)-1] + (avg_change * n_months)
    return predicted

# ---------------------------------------------------------
# [함수 정의 ⑤] apply_event(price, event_dict, event_key)
# 이벤트 계수를 반영한 조정 가격 반환
# ---------------------------------------------------------
def apply_event(price, event_dict, event_key):
    if event_key in event_dict:
        coefficient = event_dict[event_key]   # 딕셔너리에서 계수 조회
        return price * coefficient
    return price

# ---------------------------------------------------------
# [함수 정의 ⑥] draw_chart(labels, prices, unit_label)
# ---------------------------------------------------------
def draw_chart(labels, prices, unit_label):
    print()
    print("  [ 📊 시세 변화 그래프 ]")
    print("-----------------------------------------")
    max_p = max(prices)
    for i in range(len(prices)):
        bar_len = int((prices[i] / max_p) * 20)
        bar     = "█" * bar_len
        print(f"  {unit_label}{labels[i]:>2} | {bar:<20} {prices[i]:,.0f}원")
    print("-----------------------------------------")

# ---------------------------------------------------------
# [함수 정의 ⑦] save_report(goods_name, data_dict)
# 분석 결과를 txt 파일로 저장 (14주차 파일 입출력)
# ---------------------------------------------------------
def save_report(goods_name, data_dict):
    filename = f"{goods_name}_report.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"[{goods_name}] 시세 분석 리포트\n")
        f.write("=" * 40 + "\n")
        for key, value in data_dict.items():
            f.write(f"{key}: {value}\n")
    print(f"  💾 [{filename}] 저장 완료!")
    return filename

# ---------------------------------------------------------
# [함수 정의 ⑧] load_report(filename)
# 저장된 리포트 파일 불러오기 (14주차 파일 입출력)
# ---------------------------------------------------------
def load_report(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        print(content)
    except FileNotFoundError:
        print(f"  ❌ [{filename}] 파일이 없습니다.")


# =========================================================
# [이벤트 계수 딕셔너리] - 13주차 딕셔너리
# 이벤트 종류별로 가격 변동 계수를 미리 정의
# =========================================================
event_coefficients = {
    "컴백"    : 1.35,   # 컴백 시 +35% 상승
    "월드투어": 1.20,   # 월드투어 시 +20% 상승
    "스캔들"  : 0.75,   # 스캔들 시 -25% 하락
    "해체"    : 0.50,   # 해체 시 -50% 하락
    "수상"    : 1.15,   # 수상 시 +15% 상승
    "없음"    : 1.00,   # 이벤트 없음
}

# =========================================================
# 메인 프로그램 시작
# =========================================================
print("=========================================")
print("   Goods Price Trend Analyzer V4.0")
print("   다중 굿즈 시세 분석 + 파일 저장")
print("=========================================")
print()

# ---------------------------------------------------------
# [기간 단위 선택]
# ---------------------------------------------------------
print("  [기간 단위 선택]")
print("  1. 일 단위  2. 주 단위  3. 월 단위")
period_choice = input("  선택 (1/2/3): ")

if period_choice == '1':
    unit_label  = "Day "
    period_name = "일"
elif period_choice == '2':
    unit_label  = "Week"
    period_name = "주"
elif period_choice == '3':
    unit_label  = "Mon "
    period_name = "월"
else:
    unit_label  = "Week"
    period_name = "주"

count = int(input(f"  몇 {period_name}치 데이터를 입력할까요? (최소 2): "))
n_predict = int(input(f"  몇 {period_name} 뒤 가격을 예측할까요?: "))

# ---------------------------------------------------------
# [이벤트 안내]
# ---------------------------------------------------------
print()
print("  [등록된 이벤트 계수]")
for event, coef in event_coefficients.items():
    print(f"    {event}: x{coef}")

# =========================================================
# [다중 굿즈 입력]
# portfolio = { 굿즈명: { "retail": 정가, "periods": [...] } }
# 딕셔너리 안에 딕셔너리로 굿즈별 데이터를 완전히 분리해 관리
# =========================================================
portfolio = {}   # 전체 굿즈 포트폴리오 딕셔너리

print()
goods_count = int(input("분석할 굿즈 수: "))

for g in range(1, goods_count + 1):
    print()
    print(f"=========================================")
    print(f"  [{g}번째 굿즈 정보 입력]")
    print(f"=========================================")
    goods_name   = input("  굿즈 이름: ")
    retail_price = int(input("  정가(원): "))

    # 굿즈별 데이터 딕셔너리 초기화
    portfolio[goods_name] = {
        "retail"      : retail_price,
        "period_avgs" : [],
        "period_labels": [],
        "all_prices"  : [],
    }

    # ---------------------------------------------------------
    # 주차별 가격 입력
    # 가격 입력 → 바로 등록 / 빈칸 Enter → 다음 주차로
    # ---------------------------------------------------------
    for period in range(1, count + 1):
        print()
        print(f"  [{goods_name}] {period}{period_name}차 — "
              f"실거래가 입력 (빈칸 Enter = 다음 {period_name}차)")
        print(f"  ※ 이벤트 반영 가격도 입력 가능")

        period_prices = []

        while True:
            raw = input(f"    시세(원) 또는 Enter: ")

            # ★ 빈칸 Enter → break로 다음 주차로
            if raw == "":
                if len(period_prices) == 0:
                    print(f"    ⚠️  최소 1개 이상 입력해주세요.")
                    continue
                print(f"    ✔️  {period}{period_name}차 입력 완료!")
                break

            price = int(raw)

            # ★ 0 이하 입력 방지
            if price <= 0:
                print("    ⚠️  잘못된 가격입니다.")
                continue

            # 이벤트 계수 적용 여부
            print(f"    이벤트 선택: {list(event_coefficients.keys())}")
            event_key = input("    이벤트 종류 (없으면 '없음'): ")
            adjusted  = apply_event(price, event_coefficients, event_key)

            if adjusted != price:
                print(f"    🎯 이벤트 반영가: {adjusted:,.0f}원 "
                      f"(원래: {price:,}원 × {event_coefficients.get(event_key, 1.0)})")

            period_prices.append(adjusted)
            portfolio[goods_name]["all_prices"].append(adjusted)
            print(f"    ✅ {adjusted:,.0f}원 등록! "
                  f"(이번 {period_name}차 {len(period_prices)}번째 매물)")

        # 이번 주차 평균가 계산
        if len(period_prices) > 0:
            avg = sum(period_prices) / len(period_prices)
            portfolio[goods_name]["period_avgs"].append(avg)
            portfolio[goods_name]["period_labels"].append(period)


# =========================================================
# [전체 분석 리포트 + 구매 추천 정렬]
# =========================================================
print()
print("=========================================")
print("  📊 전체 굿즈 포트폴리오 분석 리포트")
print("=========================================")

# 구매 추천도 정렬용 딕셔너리
recommendation = {}   # { 굿즈명: 추천점수 }

for goods_name, data in portfolio.items():
    avgs   = data["period_avgs"]
    labels = data["period_labels"]
    retail = data["retail"]
    all_p  = data["all_prices"]

    if len(avgs) < 2:
        print(f"\n  [{goods_name}] ❌ 데이터 부족 — 분석 생략")
        continue

    global_min = min(all_p)
    global_max = max(all_p)
    global_avg = sum(all_p) / len(all_p)
    latest     = avgs[len(avgs) - 1]
    oldest     = avgs[0]
    total_rate, total_dir = get_trend(latest, oldest)
    predicted  = predict_price(avgs, n_predict)
    sell_price = get_sell_price(global_avg, global_max)
    timing_msg, score = get_timing(latest, global_min, global_avg)

    recommendation[goods_name] = score   # 추천 점수 저장

    print()
    print(f"  ┌─────────────────────────────────────")
    print(f"  │  [{goods_name}]")
    print(f"  ├─────────────────────────────────────")
    print(f"  │  정가          : {retail:,}원")
    print(f"  │  최저 실거래가 : {global_min:,}원")
    print(f"  │  최고 실거래가 : {global_max:,}원")
    print(f"  │  평균 실거래가 : {global_avg:,.0f}원")
    print(f"  │  전체 변화율   : {total_dir} {total_rate:+.1f}%")
    print(f"  ├─────────────────────────────────────")
    print(f"  │  🎯 매수 판정  : {timing_msg}")
    print(f"  │  💰 추천 판매가: {sell_price:,.0f}원")
    print(f"  │  🔮 {n_predict}{period_name} 뒤 예측가: {predicted:,.0f}원")
    print(f"  └─────────────────────────────────────")

    # 구간별 변화율
    draw_chart(labels, avgs, unit_label)

    # 파일 저장
    report_data = {
        "정가"           : f"{retail:,}원",
        "평균 실거래가"  : f"{global_avg:,.0f}원",
        "전체 변화율"    : f"{total_dir} {total_rate:+.1f}%",
        "매수 판정"      : timing_msg,
        "추천 판매가"    : f"{sell_price:,.0f}원",
        f"{n_predict}{period_name} 뒤 예측가": f"{predicted:,.0f}원",
    }
    save_report(goods_name, report_data)

# ---------------------------------------------------------
# [구매 추천 정렬] - 딕셔너리 values 기준 정렬
# ---------------------------------------------------------
print()
print("=========================================")
print("  🏆 구매 추천 순위")
print("=========================================")

# 추천 점수 높은 순으로 정렬
sorted_goods = sorted(recommendation.keys(),
                      key=lambda x: recommendation[x],
                      reverse=True)

for rank, name in enumerate(sorted_goods, 1):
    score = recommendation[name]
    if score >= 75:
        badge = "🟢 강력 추천"
    elif score >= 50:
        badge = "🟡 보통"
    else:
        badge = "🔴 비추천"
    print(f"  {rank}위. {name:<15} {badge} (점수: {score})")

print()
print("=========================================")
print("  ✨ 전체 굿즈 분석 완료!")
print("  ※ 각 굿즈별 리포트가 txt 파일로 저장되었습니다.")
print("=========================================")
