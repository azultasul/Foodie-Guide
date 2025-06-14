# Back-end code
## before we start...
please write below (with actual keys) in file `.env`
```.env
OPENAI_API_KEY=
NAVER_CLIENT_ID=
NAVER_CLIENT_SECRET=
```

## Flask + OPENAI API

## NAVER API
---
# SSL/TLS 1.3 적용
자세한 내용은 [여기](https://github.com/seonhara/Cyber-Security/blob/main/%EC%8B%A4%EC%8A%B5%EC%A0%95%EB%A6%AC/Network%20Security/TLS_example.md)를 참고하세요.
### TLS 적용 전후 비교
<p align="center">
  <img src="https://github.com/seonhara/Cyber-Security/blob/main/images/tls_before.png" alt="Image 1" height="200" width ="250" />
    &nbsp;&nbsp;&nbsp;&nbsp; <!-- 사진 사이 여백 -->
  <img src="https://github.com/seonhara/Cyber-Security/blob/main/images/tls_complete.png" alt="Image 2" height="200" width ="250" />
</p>

### TLS v1.3사용 여부 확인

```
openssl s_client -connect <도메인>:443 -tls1_3
```
s_client : SSL/TLS 서버와의 연결을 시도해서 인증서, 프로토콜 버전, 암호화 알고리즘 등을 직접 확인함

<p align="center">
<img src="https://github.com/seonhara/Cyber-Security/blob/main/images/tls1.3.png" alt="Image 1" height="200" />
</p>

---
# Secure Coding
##🔒 시큐어 코딩 기준 적용 상태
| 보안 기준 항목               | 적용 여부 |
| ---------------------- | ----- |
| ❗입력 유효성 검증             | ✅     |
| ❗비정상 입력에 대한 거부 및 오류 리턴 | ✅     |
| ❗서비스 거부(DoS) 방지        | ✅     |
| ❗타입 안정성 확보             | ✅     |

---
* Dos 공격 방지
<table>
  <tr>
    <td style="vertical-align: middle;">
      <img src="https://github.com/user-attachments/assets/0c948dea-5060-4153-b8a8-e6ed0ba1444a" height="200" width="350"/>
    </td>
    <td style="vertical-align: middle; padding-left: 20px;">
      <img src="https://github.com/user-attachments/assets/9683bc71-b68b-4109-9bb7-8f3c9d7c37fb" width = "350" height="100"/>
    </td>
  </tr>
</table>

---

* 비정상 입력에 대한 거부 및 오류 리턴
<table>
  <tr>
    <td style="vertical-align: middle;">
      <img src="https://github.com/user-attachments/assets/873384bb-abdf-4229-9600-c82546d97822" height="200" width="350"/>
    </td>
    <td style="vertical-align: middle; padding-left: 20px;">
      <img src="https://github.com/user-attachments/assets/8f845044-b629-4e23-90fb-df3253c6dacd" width = "350" height="100"/>
    </td>
  </tr>
</table>

 ---

 * 유효하지 않은 역할, 타입 안정성 확보
<table>
  <tr>
    <td style="vertical-align: middle;">
      <img src="https://github.com/user-attachments/assets/33267909-4d23-45dc-bc48-47ee584ce545" height="200" width="350"/>
    </td>
    <td style="vertical-align: middle; padding-left: 20px;">
      <img src="https://github.com/user-attachments/assets/a5c5c46d-1cec-4b82-81c7-99a8d60a3c0e" width = "350" height="200"/>
    </td>
  </tr>
</table>

---
* XSS 공격 방어
<table>
  <tr>
    <td style="vertical-align: middle;">
      <img src="https://github.com/user-attachments/assets/b04e3600-f32b-426f-ade4-9fca7d2af7d7" height="100" width="350"/>
    </td>
    <td style="vertical-align: middle; padding-left: 20px;">
      <img src="https://github.com/user-attachments/assets/a1be98a5-4964-4206-bf09-6882b9caaeed" width = "350" height="100"/>
    </td>
  </tr>
</table>




