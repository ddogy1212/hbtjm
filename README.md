# 🎂 황재민 생일 축하 사이트 — hbtjm

정적 웹사이트 + 수신 동의를 전제로 한 **1명 대상 생일 자동 알림 설정 예제**입니다.

## 사이트에서 바로 되는 기능
- 생일 축하 문구와 폭죽 애니메이션
- 100 / 500 / 1,000 / 3,000줄 클립보드 복사
- 브라우저가 열려 있는 동안 허용된 **내 기기 알림** 최대 12회
- Android/iPhone 공유 메뉴로 가능한 앱 선택
- 동의한 수신자의 **문자·이메일 작성창** 열기
- 인스타그램 DM 열기 + 축하 문구 복사

문자·메일 작성창과 기기의 공유 메뉴는 **자동 발송이 아닙니다.** 최종 보내기를 눌러야 합니다.

## GitHub Pages 공개
1. GitHub `ddogy1212/hbtjm` 저장소 → **Settings** → **Pages**
2. **Build and deployment** → **Deploy from a branch**
3. **main / (root)** 선택 후 **Save**
4. 게시 완료 후 `https://ddogy1212.github.io/hbtjm/` 접속

게시 설정과 HTTPS 반영이 끝나기 전에는 주소에 접속할 수 없을 수 있습니다.

## GitHub Actions에서 생일 당일 자동으로 1회 보내기

`.github/workflows/birthday-auto.yml`과 `scripts/send_birthday.py`를 제공합니다. 매일 한국시간 00:10 전후에 실행하되, **등록한 생일과 일치할 때만** 전송을 시도합니다. GitHub Actions 예약 실행에는 지연이 있을 수 있으며 수신 성공을 보장하지 않습니다.

**아직 연동 인증정보는 등록되지 않았으므로 실제 문자·이메일은 자동으로 발송되지 않습니다.**

저장소 Settings → Secrets and variables → Actions에서 다음을 설정하세요.

### Variables (일반 변수)
- `BIRTHDAY_MMDD`: 실제 생일을 `MM-DD` 형식으로 (예: `02-12`).
- `CONSENT_CONFIRMED`: 본인 또는 수신 당사자의 명확한 동의가 있다면 `yes`.
- `SMTP_HOST`: 메일 서버 주소 (미설정이면 gmail SMTP)
- `SMTP_PORT`: SSL SMTP 포트 (미설정이면 `465`)

### Secrets (비밀 값)
**이메일 (SMTP):**
- `TARGET_EMAIL` : 메일 받을 **동의한 한 사람의 주소**
- `SMTP_USER` : SMTP 로그인 계정 / 발신 주소
- `SMTP_PASSWORD` : SMTP 인증 비밀번호

**SMS (Twilio API, 선택):**
- `TARGET_PHONE` : 동의한 수신자 **한 명**의 번호, E.164 형식 (예: `+821012345678`)
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM` : 문자 발신용 Twilio 번호

일반 휴대전화에 저장된 모든 연락처를 수집하지 않습니다. 수신자 리스트 대량 전송 기능도 없습니다. 인스타그램 개인 계정 DM 자동화는 제공하지 않습니다.

**테스트:** GitHub → Actions → "Birthday - consented self messages" → Run workflow. 생일·동의 변수가 맞아야 전송됩니다. 연속 수동 실행은 재발송으로 이어질 수 있으니 주의하세요.

**보안:** 공개 저장소 코드나 파일에 전화번호, 이메일, SMTP 비밀번호, Twilio 토큰을 직접 적지 마세요. GitHub Secrets를 사용하세요. 사용량과 통신 비용은 해당 외부 서비스 정책에 따릅니다.
