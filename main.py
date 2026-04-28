# 파일이름 :굿즈 수집가를 위한 중고장터 시세 분석 및 매매 타이밍 도우미
# 작 성 자 :남현빈
# =========================================================
# [Resell-Master V2.0] 굿즈 시세 분석 + 가성비 판정 프로그램
# 작성자: 남현빈
# 과제 목표: 리스트 입력/조작, 조건문(if-elif-else, 중첩 if),
#            연산자(관계, 논리, 대입), break, continue, f-string 출력
# =========================================================

print("=========================================")
print("     Goods Market Analyzer V2.0")
print("   굿즈 시세 분석 + 가성비 판정 시스템")
print("=========================================")
print()

# ---------------------------------------------------------
# [변수 선언] - int, float, str 자료형 포함, 5개 이상
# ---------------------------------------------------------
owner_name: str = input("수집가 닉네임을 입력하세요: ")      # 문자열(str)
budget: int = int(input("오늘의 예산(원): "))                 # 정수(int)
target_profit_rate: float = float(input("목표 수익률(%): "))  # 실수(float)
total_spent: int = 0       # 총 지출 (대입연산자로 누적 예정)
valid_count: int = 0       # 유효하게 입력된 굿즈 수

print()
print("-----------------------------------------")
print("  굿즈 정보를 3개 입력해주세요")
print("  ※ 시세가 0원 이하이면 자동으로 건너뜁니다 (continue)")
print("-----------------------------------------")

# ---------------------------------------------------------
# [리스트 준비] - 빈 리스트 생성
# ---------------------------------------------------------
goods_names   = []   # 굿즈 이름
retail_prices = []   # 정가
market_prices = []   # 현재 시세

# ---------------------------------------------------------
# [리스트 입력 + for + continue] - 잘못된 데이터 스킵
# ---------------------------------------------------------
for i in range(3):
    print(f"\n  [{i+1}번째 굿즈]")
    name   = input("    굿즈 이름: ")
    retail = int(input("    정가(원): "))
    market = int(input("    현재 시세(원): "))

    # ★ continue: 시세가 0 이하면 불량 데이터로 판단 → 이번 회차 스킵
    if market <= 0 or retail <= 0:
        print("    ⚠️  시세 또는 정가가 0원 이하입니다. 이 굿즈는 건너뜁니다. (continue)")
        continue

    goods_names.append(name)
    retail_prices.append(retail)
    market_prices.append(market)

    total_spent += market      # 복합 대입 연산자 +=
    valid_count += 1

print()

# ---------------------------------------------------------
# [리스트 조작] - insert, sort, index, len, sum, max
# ---------------------------------------------------------
hot_item = input("현재 가장 주목받는 '관심 급등 굿즈' 이름을 입력하세요: ")
goods_names.insert(0, hot_item)   # insert 사용

sorted_prices = market_prices[:]
sorted_prices.sort()              # sort 사용

total_items   = len(goods_names)  # len 사용
total_market  = sum(market_prices)  # sum 사용 (유효 굿즈만)
highest_price = max(market_prices)  # max 사용
highest_index = market_prices.index(highest_price)  # index 사용

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
print("  ※ 심각한 거품(시세가 정가의 2배 초과) 발견 시 즉시 경보! (break)")
print("-----------------------------------------")

# ---------------------------------------------------------
# [제어구조 ②] for + if-elif-else + break: 거품 위험 경보
# [연산자] 관계연산자(>) , 논리연산자(and, or)
# ---------------------------------------------------------
for i in range(valid_count):
    ratio = market_prices[i] / retail_prices[i]
    profit = market_prices[i] - retail_prices[i]
    profit_rate = (profit / retail_prices[i]) * 100

    # 연속 if-elif-else (가성비 등급)
    if ratio <= 1.0:
        grade = "🟢 혜자"
        advice = "지금 당장 매수 추천!"
    elif ratio <= 1.3:
        grade = "🟡 적정"
        advice = "시세가 안정적입니다."
    elif ratio <= 1.8:
        grade = "🟠 거품 주의"
        advice = "조금 더 기다려보세요."
    else:
        grade = "🔴 심각한 거품"
        advice = "매수 비추천!"

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

    # ★ break: 시세가 정가의 2배를 초과하면 위험 경보 후 분석 즉시 중단
    if ratio > 2.0:
        print()
        print("  🚨🚨🚨 위험 경보! 🚨🚨🚨")
        print(f"  [{goods_names[i+1]}] 의 시세가 정가의 {ratio:.1f}배를 초과했습니다!")
        print("  나머지 굿즈 분석을 즉시 중단합니다. (break)")
        print("  포트폴리오를 재점검하세요!")
        break

print()
print("=========================================")
print(f"  ✨ {owner_name}님의 분석 완료!")
print("  ※ V3.0: 반복 메뉴 + 실시간 시세 감시 기능 추가 예정")
print("=========================================")
