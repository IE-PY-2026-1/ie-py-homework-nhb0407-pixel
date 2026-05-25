# =========================================================
# [Resell-Master V3.0] 굿즈 시세 추이 분석기
# 작성자: 남현빈
# 핵심 기능: 기간별 시세 변화율, 상승/하락 추이,
#            허수 시세 제거, 매수 타이밍 판단
#            + 주차별 다중 매물 입력
# =========================================================

# ---------------------------------------------------------
# [함수 정의 ①] get_trend(current, previous)
# 현재가와 이전가를 받아 변화율(%)과 방향을 반환
# ---------------------------------------------------------
def get_trend(current, previous):
    rate = (current - previous) / previous * 100
    if rate > 0:
        direction = "📈 상승"
    elif rate < 0:
        direction = "📉 하락"
    else:
        direction = "➡️  보합"
    return rate, direction

# ---------------------------------------------------------
# [함수 정의 ②] get_timing(latest, min_price, avg_price)
# 최저가/평균가 기반으로 매수 타이밍 판단 후 반환
# ---------------------------------------------------------
def get_timing(latest_price, min_price, avg_price):
    ratio_to_avg = (latest_price / avg_price) * 100
    if latest_price <= min_price:
        return "🟢 역대 최저가! 지금이 최적 매수 타이밍!"
    elif ratio_to_avg <= 90:
        return "🟡 평균가보다 10% 이상 저렴 — 매수 고려해볼 만해요"
    elif ratio_to_avg <= 105:
        return "🟠 평균가 근처 — 조금 더 지켜보세요"
    else:
        return "🔴 평균가보다 많이 높음 — 매수 비추천"

# ---------------------------------------------------------
# [함수 정의 ③] get_real_avg(prices, statuses)
# 거래완료 매물만 필터링해서 평균가 반환
# ---------------------------------------------------------
def get_real_avg(prices, statuses):
    real = []
    for i in range(len(prices)):
        if statuses[i] == '1':          # 거래완료만
            real.append(prices[i])
    if len(real) == 0:
        return 0, real
    avg = sum(real) / len(real)
    return avg, real                    # 평균가, 실거래 리스트 반환

# ---------------------------------------------------------
# [함수 정의 ④] draw_chart(labels, prices, unit_label)
# 텍스트 막대 그래프 출력
# ---------------------------------------------------------
def draw_chart(labels, prices, unit_label):
    print()
    print("  [ 📊 주차별 평균 실거래가 그래프 ]")
    print("-----------------------------------------")
    max_p = max(prices)
    for i in range(len(prices)):
        bar_len = int((prices[i] / max_p) * 20)
        bar     = "█" * bar_len
        print(f"  {unit_label}{labels[i]:>2} | {bar:<20} {prices[i]:,.0f}원")
    print("-----------------------------------------")


# =========================================================
# 메인 프로그램 시작
# =========================================================
print("=========================================")
print("   Goods Price Trend Analyzer V3.0")
print("   굿즈 시세 추이 분석 + 매수 타이밍")
print("=========================================")
print()

# ---------------------------------------------------------
# [기본 정보 입력]
# ---------------------------------------------------------
goods_name   = input("분석할 굿즈 이름: ")
retail_price = int(input("정가(원): "))

print()
print("  [기간 단위 선택]")
print("  1. 일 단위")
print("  2. 주 단위")
print("  3. 월 단위")
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
    print("  ⚠️  잘못된 선택. 주 단위로 설정합니다.")
    unit_label  = "Week"
    period_name = "주"

count = int(input(f"  몇 {period_name}치 데이터를 입력할까요? (최소 2): "))

# ---------------------------------------------------------
# [데이터 저장용 리스트]
# period_avgs  : 주차별 실거래 평균가 (추이 분석용)
# period_labels: 주차 번호
# total_real   : 전체 실거래가 모음 (전체 통계용)
# total_fake   : 전체 허수 매물 수
# ---------------------------------------------------------
period_avgs   = []
period_labels = []
total_real    = []
total_fake    = 0

# =========================================================
# [핵심] 주차별 매물 입력 루프
# 바깥 for  : 주차 반복 (1주차 ~ N주차)
# 안쪽 while: 해당 주차 매물 계속 추가
# =========================================================
for period in range(1, count + 1):

    print()
    print(f"=========================================")
    print(f"  [{period}{period_name}차] 매물 입력")
    print(f"  ※ 매물 추가 → 1  |  다음 {period_name}차로 → 2")
    print(f"=========================================")

    period_prices   = []   # 이번 주차 전체 가격
    period_statuses = []   # 이번 주차 전체 상태
    listing_num     = 0    # 이번 주차 매물 번호

    # ★ while True: 매물을 계속 입력받는 무한루프
    while True:
        listing_num += 1
        print(f"\n  [{period}{period_name}차 - {listing_num}번 매물]")
        price  = int(input("    시세(원): "))
        status = input("    매물 상태 (1=거래완료 / 2=판매중): ")

        # ★ continue: 가격 0 이하면 잘못된 입력으로 스킵
        if price <= 0:
            print("    ⚠️  잘못된 가격입니다. 다시 입력해주세요.")
            listing_num -= 1    # 번호 차감 (유효 매물 아니므로)
            continue

        period_prices.append(price)
        period_statuses.append(status)

        if status == '1':
            print(f"    ✅ 거래완료 매물 등록!")
        else:
            print(f"    🚫 판매중(허수) 매물 등록")

        # 추가 or 다음 주차 선택
        print()
        print(f"  ─────────────────────────────────")
        print(f"  1. 매물 추가 입력")
        print(f"  2. {period}{period_name}차 입력 완료 → 다음으로")
        print(f"  ─────────────────────────────────")
        next_action = input("  선택: ")

        # ★ break: 다음 주차로 넘어가기 선택 시 while 탈출
        if next_action == '2':
            print(f"  ✔️  {period}{period_name}차 입력 완료!")
            break
        elif next_action != '1':
            # 잘못된 입력이면 continue로 다시 선택
            print("  ⚠️  잘못된 선택입니다. 매물 추가로 진행합니다.")

    # ---------------------------------------------------------
    # 이번 주차 마무리 처리
    # get_real_avg() 함수로 허수 제거 후 평균가 계산
    # ---------------------------------------------------------
    avg, real_list = get_real_avg(period_prices, period_statuses)
    fake_this      = len(period_prices) - len(real_list)
    total_fake    += fake_this

    print()
    print(f"  [{period}{period_name}차 요약]")
    print(f"  전체 매물    : {len(period_prices)}개")
    print(f"  거래완료     : {len(real_list)}개  |  허수(판매중): {fake_this}개")

    if len(real_list) == 0:
        print(f"  ⚠️  실거래 매물 없음 — 이번 {period_name}차는 분석에서 제외됩니다.")
    else:
        print(f"  실거래 평균가: {avg:,.0f}원")
        print(f"  실거래 범위  : {min(real_list):,}원 ~ {max(real_list):,}원")
        period_avgs.append(avg)
        period_labels.append(period)
        total_real.extend(real_list)    # 전체 실거래 리스트에 합산


# =========================================================
# [전체 분석 리포트]
# =========================================================
print()
print("=========================================")
print(f"  [{goods_name}] 전체 시세 추이 분석 리포트")
print("=========================================")

if len(period_avgs) < 2:
    print("  ❌ 분석 가능한 실거래 데이터가 부족합니다.")
    print(f"  (최소 2개 {period_name}차의 실거래 데이터 필요)")

else:
    # 전체 통계
    global_min = min(total_real)
    global_max = max(total_real)
    global_avg = sum(total_real) / len(total_real)
    latest_avg = period_avgs[len(period_avgs) - 1]
    oldest_avg = period_avgs[0]
    total_rate, total_dir = get_trend(latest_avg, oldest_avg)

    print(f"  정가              : {retail_price:,}원")
    print(f"  분석 {period_name}차 수      : {len(period_avgs)}{period_name} (실거래 기준)")
    print(f"  전체 실거래 건수  : {len(total_real)}건")
    print(f"  허수 제거 건수    : {total_fake}건")
    print(f"  전체 최저 실거래가: {global_min:,}원")
    print(f"  전체 최고 실거래가: {global_max:,}원")
    print(f"  전체 평균 실거래가: {global_avg:,.0f}원")
    print(f"  최초 평균가       : {oldest_avg:,.0f}원")
    print(f"  최근 평균가       : {latest_avg:,.0f}원")
    print(f"  전체 변화율       : {total_dir} {total_rate:+.1f}%")

    # ---------------------------------------------------------
    # [구간별 변화율] for + get_trend()
    # ---------------------------------------------------------
    print()
    print(f"  [ 구간별 {period_name}차 평균가 변화율 ]")
    print("-----------------------------------------")

    up_count   = 0
    down_count = 0
    flat_count = 0
    max_up     = 0.0
    max_down   = 0.0

    for i in range(1, len(period_avgs)):
        rate, direction = get_trend(period_avgs[i], period_avgs[i-1])
        print(f"  {unit_label}{period_labels[i-1]:>2} → "
              f"{unit_label}{period_labels[i]:>2} : "
              f"{direction} {rate:+.1f}%  "
              f"({period_avgs[i-1]:,.0f}원 → {period_avgs[i]:,.0f}원)")

        if rate > 0:
            up_count += 1
            if rate > max_up:
                max_up = rate
        elif rate < 0:
            down_count += 1
            if rate < max_down:
                max_down = rate
        else:
            flat_count += 1

    # ---------------------------------------------------------
    # [추이 요약]
    # ---------------------------------------------------------
    print()
    print("  [ 추이 요약 ]")
    print("-----------------------------------------")
    print(f"  📈 상승 구간 : {up_count}회  (최대 {max_up:+.1f}%)")
    print(f"  📉 하락 구간 : {down_count}회  (최대 {max_down:+.1f}%)")
    print(f"  ➡️  보합 구간 : {flat_count}회")

    # 전체 추세 판단
    if up_count > down_count and total_rate > 0:
        trend_summary = "📈 전반적 상승세 — 팔기 좋은 시장입니다."
    elif down_count > up_count and total_rate < 0:
        trend_summary = "📉 전반적 하락세 — 매수 기회를 노려보세요."
    elif up_count == down_count or abs(total_rate) <= 3.0:
        trend_summary = "➡️  횡보 중 — 관망하며 추가 데이터를 기다리세요."
    else:
        trend_summary = "🔀 혼조세 — 단기 변동성이 높습니다."

    print(f"\n  종합 추세: {trend_summary}")

    # ---------------------------------------------------------
    # [텍스트 차트] draw_chart()
    # ---------------------------------------------------------
    draw_chart(period_labels, period_avgs, unit_label)

    # ---------------------------------------------------------
    # [매수 타이밍 판단] get_timing()
    # ---------------------------------------------------------
    timing = get_timing(latest_avg, global_min, global_avg)
    ratio_to_retail = (latest_avg / retail_price) * 100

    print()
    print("  [ 🎯 매수 타이밍 판단 ]")
    print("-----------------------------------------")
    print(f"  최근 {period_name}차 평균 실거래가 : {latest_avg:,.0f}원")
    print(f"  정가 대비              : {ratio_to_retail:.1f}%")
    print(f"  판정 결과              : {timing}")

    # 반등 감지 (직전 2구간 데이터 필요)
    if len(period_avgs) >= 3:
        last_rate, _ = get_trend(
            period_avgs[len(period_avgs) - 1],
            period_avgs[len(period_avgs) - 2]
        )
        prev_rate, _ = get_trend(
            period_avgs[len(period_avgs) - 2],
            period_avgs[len(period_avgs) - 3]
        )
        if prev_rate < 0 and last_rate > 0:
            print(f"  🚀 직전 하락 후 반등 감지! 매수 타이밍 신호!")
        elif prev_rate > 0 and last_rate < 0:
            print(f"  ⚠️  직전 상승 후 하락 전환 — 매수 보류 권장")

    print()
    print("=========================================")
    print(f"  ✨ [{goods_name}] 분석 완료!")
    print("=========================================")
