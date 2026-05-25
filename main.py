# 파일이름 : 굿즈 수집가를 위한 중고장터 시세 분석 및 매매 타이밍 도우미
# 작 성 자 : 남현빈
# =========================================================
# [Resell-Master V2.1] 굿즈 시세 분석 + 가성비 판정 프로그램
# 과제 목표: 리스트 입력/조작, 조건문(if-elif-else, 중첩 if),
#            연산자(관계, 논리, 대입), break, continue, f-string 출력
#            + def 함수 분리, 기본값 인수, count() 집계, in 중복 방지
# =========================================================

# ---------------------------------------------------------
# [함수 정의 ①] get_grade(ratio) - 11주차
# ratio 값을 받아 가성비 등급 문자열을 return
# ---------------------------------------------------------
def get_grade(ratio):
    if ratio <= 1.0:
        return "🟢 혜자"
    elif ratio <= 1.3:
        return "🟡 적정"
    elif ratio <= 1.8:
        return "🟠 거품 주의"
    else:
        return "🔴 심각한 거품"

# ---------------------------------------------------------
# [함수 정의 ②] calc_profit_rate(retail, market) - 11주차
# 정가와 시세를 받아 수익률(%)을 return
# ---------------------------------------------------------
def calc_profit_rate(retail, market):
    profit = market - retail
    rate   = (profit / retail) * 100
    return rate

# ---------------------------------------------------------
# [함수 정의 ③] is_danger(ratio, limit=2.0) - 12주차 기본값 인수
# 거품 경보 기준을 기본값 2.0으로 설정, 필요 시 변경 가능
# ---------------------------------------------------------
def is_danger(ratio, limit=2.0):
    return ratio > limit


# ---------------------------------------------------------
# 인트로 출력
# ---------------------------------------------------------
print("=========================================")
print("     Goods Market Analyzer V2.1")
print("   굿즈 시세 분석 + 가성비 판정 시스템")
print("=========================================")
print()

# ---------------------------------------------------------
# [변수 선언] - int, float, str 자료형 포함, 5개 이상
# ---------------------------------------------------------
owner_name         = input("수집가 닉네임을 입력하세요: ")     # str
budget             = int(input("오늘의 예산(원): "))            # int
target_profit_rate = float(input("목표 수익률(%): "))           # float
danger_limit       = float(input("거품 경보 기준 배율 (기본 2.0): ") or "2.0")  # float
total_spent        = 0    # int - 복합 대입 연산자로 누적
valid_count        = 0    # int - 유효하게 입력된 굿즈 수

print()
print("-----------------------------------------")
print("  굿즈 정보를 3개 입력해주세요")
print("  ※ 시세가 0원 이하 → 자동 건너뜀 (continue)")
print("  ※ 이미 등록된 이름 → 중복 방지 (in + continue)")
print("-----------------------------------------")

# ---------------------------------------------------------
# [리스트 준비]
# ---------------------------------------------------------
goods_names   = []   # 굿즈 이름
retail_prices = []   # 정가
market_prices = []   # 현재 시세
grade_log     = []   # ★ 등급 결과 저장용 리스트 (count() 집계에 사용)

# ---------------------------------------------------------
# [리스트 입력 + for + continue]
# ---------------------------------------------------------
for i in range(3):
    print(f"\n  [{i+1}번째 굿즈]")
    name   = input("    굿즈 이름: ")
    retail = int(input("    정가(원): "))
    market = int(input("    현재 시세(원): "))

    # ★ in 연산자: 이미 등록된 이름이면 중복 방지 후 continue
    if name in goods_names:
        print(f"    ⚠️  [{name}]은 이미 등록된 굿즈입니다. 건너뜁니다. (in + continue)")
        continue

    # ★ continue: 시세 또는 정가가 0 이하면 불량 데이터 스킵
    if market <= 0 or retail <= 0:
        print("    ⚠️  시세 또는 정가가 0원 이하입니다. 건너뜁니다. (continue)")
        continue

    goods_names.append(name)
    retail_prices.append(retail)
    market_prices.append(market)

    total_spent += market    # 복합 대입 연산자 +=
    valid_count += 1

print()

# ---------------------------------------------------------
# [리스트 조작] - insert, sort, index, len, sum, max
# ---------------------------------------------------------
hot_item = input("현재 가장 주목받는 '관심 급등 굿즈' 이름을 입력하세요: ")
goods_names.insert(0, hot_item)

sorted_prices = market_prices[:]
sorted_prices.sort()

total_items   = len(goods_names)
total_market  = sum(market_prices)
highest_price = max(market_prices)
highest_index = market_prices.index(highest_price)

print()
print("=========================================")
print(f"  [{owner_name}] 굿즈 포트폴리오 분석 리포트")
print("=========================================")
print(f"  등록된 굿즈 수       : {valid_count}개 (유효 데이터만)")
print(f"  총 시세 합계         : {total_market:,}원")
print(f"  가장 비싼 시세       : {highest_price:,}원 ({goods_names[highest_index+1]})")
print(f"  시세 오름차순 정렬   : {sorted_prices}")
print(f"  오늘 예산            : {budget:,}원")
print(f"  총 지출              : {total_spent:,}원")
print()

# ---------------------------------------------------------
# [제어구조 ①] if-elif-else: 예산 초과 여부 판단
# ---------------------------------------------------------
remaining = budget - total_spent

if remaining > 0:
    print(f"  ✅ 예산 여유 있음! 잔여 예산: {remaining:,}원")
elif remaining == 0:
    print(f"  ⚠️  예산을 딱 맞게 사용했습니다.")
else:
    over = total_spent - budget
    print(f"  ❌ 예산 초과! {over:,}원 부족합니다.")

print()
print("-----------------------------------------")
print("  굿즈별 가성비(거품) 분석")
print(f"  ※ 거품 경보 기준: 정가의 {danger_limit}배 초과 시 즉시 중단! (break)")
print("-----------------------------------------")

# ---------------------------------------------------------
# [제어구조 ②] for + if-elif-else + break: 거품 위험 경보
# ★ get_grade(), calc_profit_rate(), is_danger() 함수 호출
# ---------------------------------------------------------
for i in range(valid_count):
    ratio       = market_prices[i] / retail_prices[i]
    profit_rate = calc_profit_rate(retail_prices[i], market_prices[i])  # ★ 함수 호출
    grade       = get_grade(ratio)                                       # ★ 함수 호출
    advice      = ""

    # 등급별 조언 설정
    if grade == "🟢 혜자":
        advice = "지금 당장 매수 추천!"
    elif grade == "🟡 적정":
        advice = "시세가 안정적입니다."
    elif grade == "🟠 거품 주의":
        advice = "조금 더 기다려보세요."
    else:
        advice = "매수 비추천!"

    grade_log.append(grade)    # ★ 등급 결과 리스트에 저장

    print(f"\n  [{goods_names[i+1]}]")
    print(f"    정가: {retail_prices[i]:,}원 | 시세: {market_prices[i]:,}원")
    print(f"    가성비 비율: {ratio:.2f}배 → {grade}")
    print(f"    예상 수익률: {profit_rate:.1f}%")
    print(f"    💬 조언: {advice}")

    # [중첩 if] 논리연산자 and, or 사용
    if profit_rate >= target_profit_rate and remaining > 0:
        print(f"    🚀 목표 수익률({target_profit_rate}%) 달성! 매도 타이밍입니다.")
    elif profit_rate >= target_profit_rate or ratio <= 1.0:
        print(f"    📌 수익 또는 혜자 조건 중 하나 충족 — 관심 유지!")
    else:
        if ratio > 1.8:
            print(f"    ⛔ 거품이 심각합니다. 관망하세요.")

    # ★ is_danger() 함수 호출 - 기본값 인수로 기준 전달
    if is_danger(ratio, limit=danger_limit):
        print()
        print("  🚨🚨🚨 위험 경보! 🚨🚨🚨")
        print(f"  [{goods_names[i+1]}] 의 시세가 정가의 {ratio:.1f}배를 초과했습니다!")
        print(f"  설정 기준: {danger_limit}배 초과 → 분석 즉시 중단! (break)")
        print("  포트폴리오를 재점검하세요!")
        grade_log.append(grade)   # break 전에도 등급 기록
        break

# ---------------------------------------------------------
# ★ [등급 집계] count() 메소드로 각 등급 개수 출력 - 10주차
# ---------------------------------------------------------
print()
print("-----------------------------------------")
print("  📊 등급 집계 결과")
print("-----------------------------------------")
print(f"  🟢 혜자       : {grade_log.count('🟢 혜자')}개")
print(f"  🟡 적정       : {grade_log.count('🟡 적정')}개")
print(f"  🟠 거품 주의  : {grade_log.count('🟠 거품 주의')}개")
print(f"  🔴 심각한 거품: {grade_log.count('🔴 심각한 거품')}개")
print(f"  📦 분석 완료  : 총 {len(grade_log)}개")

print()
print("=========================================")
print(f"  ✨ {owner_name}님의 분석 완료!")
print("  ※ V3.0: 반복 메뉴 + 실시간 시세 감시 기능 추가 예정")
print("=========================================")
