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



