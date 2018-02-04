# StyleTransfer
Tensorflow code for "A Neural Algorithm of Artistic Style" (arXiv 1506.06576) 

## 논문 정리 및 메모
블로그정리
http://artoria.us/17
### Optimize 방법
Style Transfer 알고리즘  
input은 은 두가지
- I content
- I style

그리고 I style/content의 피쳐 맵을 추출해서 
I output의 픽셀들을 Optimize 한다.
- content의 피쳐 맵이 I content의 피쳐 맵과 유사해지도록  
- style 피쳐 맵들이 I style의 피쳐 맵과 유사해지도록

네트워크를 optimize 하는게 아니라 I output의 픽셀을 Optimize

### 목적함수 설명
L content는 Content의 Loss  
L style은 Style의 Loss

- Fl ==> I output의 l 번쨰 레이어의 피쳐맵
- Pl ==> I content의 l 번쨰 레이어의 피쳐맵
- Sl ==> I style의 l 번쨰 레이어의 피쳐맵

콘텐츠 로스는 다음과 같이 정의된다.  
```L content = Sum(Fl - Pl)^2```  
이 식은 출력과 콘텐츠 이미지의 각각의 레이어에 대한 피쳐맵간의 Frobenius Norm의 제곱을 의미한다.


이떄 비교하는피쳐맵은 핵심적인 정보가 살아있는 깊은 층의 피쳐맵을 사용한다.

스타일 로스는 다음과 같이 정의된다.  
```L style = Sum(W * Sum(Gram(Fl) - Gram(Sl)))```  
스타일 로스는 피쳐맵에 대해 Gram 행렬을 구한 후 Frobenius Norm의 제곱을 한 후 가중치w를 곱한 Sum을 구한다.

최종 목적 함수는 다음과 같다  
```Min[I output] L totoal = Min[I output]((Alpha * L content) + (Beta * L style))```  
Alpha와 Beta는 각각의 로스에 가중치를 주는 변수로 이 가중치에 따라 출력이 스타일 중점인지, 콘텐츠 중심인지 결정된다.

## References
[Style Transfer](https://blog.lunit.io/2017/04/27/style-transfer/)
[Gram matrix](https://ko.wikipedia.org/wiki/그람_행렬)
