## 정규식 사용 순서

1. p = re.compile('<b>원하는 형태</b>')<br>
2.
    2-1. m = p.match('비교할 문자열') : 주어진 문자열의 처음부터 일치하는지 확인<br>
    2-2. m = p.search('비교할 문자열') : 주어진 문자열 중에 일치하는게 있는지 확인<br>
    2-3. m = p.findall('비교할 문자열') : 일치하는 모든 것을 "리스트" 형태로 반환<br>


#### 원하는 형태
- . : (ca.e) : 하나의 문자를 의미 > care, cafe, case (O) | caffe (X) <br>
- ^ : (^de) : 문자열의 시작 > desk, destination (O) | fade (X) <br>
- $ : (se $ ) : 문자열의 끝 > case, base (O) | face (X) <br>