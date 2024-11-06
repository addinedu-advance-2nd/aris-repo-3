DROP DATABASE BARTENDROID;

CREATE DATABASE BARTENDROID;

USE BARTENDROID;

CREATE TABLE CUSTOMER (
	ID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (ID)
);

CREATE TABLE REQUEST (
	ID INT NOT NULL AUTO_INCREMENT,
    TOTAL_PRICE INT NOT NULL,
    REQUEST_DT DATETIME NOT NULL DEFAULT NOW(),
    CUSTOMER_ID INT NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMER(ID)
);

CREATE TABLE ICECREAM (
	ID INT NOT NULL AUTO_INCREMENT,
    CATEGORY VARCHAR(20) NOT NULL,
    NAME VARCHAR(20) NOT NULL,
    PRICE INT NOT NULL,
    IMG VARCHAR(255) NOT NULL,
    STATUS BOOLEAN NOT NULL DEFAULT 1,
    PRIMARY KEY (ID)
);

CREATE TABLE TOPPING (
	ID INT NOT NULL AUTO_INCREMENT,
    NAME VARCHAR(20) NOT NULL,
    PRICE INT NOT NULL,
    IMG VARCHAR(255) NOT NULL,
    STATUS BOOL NOT NULL DEFAULT 1,
    PRIMARY KEY (ID)
);

CREATE TABLE MENU (
	ID INT NOT NULL AUTO_INCREMENT,
    REQUEST_ID INT NOT NULL,
    ICECREAM_ID INT NOT NULL,
    TOPPING_ID INT NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (REQUEST_ID) REFERENCES REQUEST(ID),
    FOREIGN KEY (ICECREAM_ID) REFERENCES ICECREAM(ID),
    FOREIGN KEY (TOPPING_ID) REFERENCES TOPPING(ID)
);

# ICECREAM DATA INSERTION
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('스페셜','치토스 밀크쉐이크 아이스크림',5000,'https://www.baskinrobbins.co.kr/upload/product/main/6b7de3ba55a71e3e99dc341d5cb908a9.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','너 T(tea)야??',5000,'https://www.baskinrobbins.co.kr/upload/product/main/d07eb9cc2b781a21cfa3f18932473478.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','내가 아인슈페너?!',5000,'https://www.baskinrobbins.co.kr/upload/product/main/19bf954288abc59f184a75737ab9d720.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('스페셜','쫀떡궁합',5000,'https://www.baskinrobbins.co.kr/upload/product/main/9368bad2b705ebb121e4b1f9f0e1c57e.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('과일','나주배 소르베',5000,'https://www.baskinrobbins.co.kr/upload/product/main/1db88b4ce08086f487c72ef55344558a.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('과일','블루베리 파나코타',5000,'https://www.baskinrobbins.co.kr/upload/product/main/7f981fc6e7a526daee600f4cee803b43.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('플레인','소금 우유 아이스크림',5000,'https://www.baskinrobbins.co.kr/upload/product/main/719e8584fd50151284b5ace3589f7a34.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','봉쥬르, 마카롱',5000,'https://www.baskinrobbins.co.kr/upload/product/main/0b22f758c9d1d0551498caafc4512f5c.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('과일','알폰소 망고',5000,'https://www.baskinrobbins.co.kr/upload/product/main/df7fdd6f667571b6521ae17cd27e3843.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('과일','애플 민트',5000,'https://www.baskinrobbins.co.kr/upload/product/main/eec8cef386cf6697768a89b384c07bf7.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('스페셜','너는 참 달고나',5000,'https://www.baskinrobbins.co.kr/upload/product/main/cc95113a4bfca780bbfee39b16fbedf1.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','마법사의 비밀 레시피',5000,'https://www.baskinrobbins.co.kr/upload/product/main/dd743197f80c722eb57389b4c1814d2f.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','엄마는 외계인',5000,'https://www.baskinrobbins.co.kr/upload/product/main/91c8668227bcf556c43a968b97e342e6.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','민트 초콜릿 칩',5000,'https://www.baskinrobbins.co.kr/upload/product/main/fb92d70dee836652115c4f3b13175541.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('스페셜','뉴욕 치즈케이크',5000,'https://www.baskinrobbins.co.kr/upload/product/main/60a04a3a5d1b0119f065d12ee7797b2c.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('과일','레인보우 샤베트',5000,'https://www.baskinrobbins.co.kr/upload/product/main/5ad63f3af7244a666d981a1497a39fe7.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('과일','체리쥬빌레',5000,'https://www.baskinrobbins.co.kr/upload/product/main/f6609e3e3431d54beceeb1d3787403af.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('스페셜','슈팅스타',5000,'https://www.baskinrobbins.co.kr/upload/product/main/a4b71e8b99743c93a7824331850b0a3d.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('과일','사랑에 빠진 딸기',5000,'https://www.baskinrobbins.co.kr/upload/product/main/387609a495e841413a453ce22b555840.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','오레오 쿠키 앤 크림',5000,'https://www.baskinrobbins.co.kr/upload/product/main/414246bd9041530d6ad4d30d97aac87c.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('과일','베리베리 스트로베리',5000,'https://www.baskinrobbins.co.kr/upload/product/main/ea6608b4f72563b360da5c44c946ddc7.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('스페셜','31요거트',5000,'https://www.baskinrobbins.co.kr/upload/product/main/d56328637eaf86e3273ebc39c57aada7.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('과일','바람과 함께 사라지다',5000,'https://www.baskinrobbins.co.kr/upload/product/main/01ecc320f5d3a6f32e5188eda373842d.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('스페셜','이상한 나라의 솜사탕',5000,'https://www.baskinrobbins.co.kr/upload/product/main/4db4f9967ad6f603837a40eede965ef0.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('스페셜','피스타치오 아몬드',5000,'https://www.baskinrobbins.co.kr/upload/product/main/868364b0ed6038d0c9aee0a10e50d4a9.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','초콜릿 무스',5000,'https://www.baskinrobbins.co.kr/upload/product/main/0d67607c2ca4dde4ec24ac8109a343c2.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('플레인','그린티',5000,'https://www.baskinrobbins.co.kr/upload/product/main/a6bd7bcdd6bdb56f28df7e98f051abda.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('스페셜','찰떡이구마',5000,'https://www.baskinrobbins.co.kr/upload/product/main/69f8fcb8dadccc84a8ad1f86d203decd.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','초콜릿',5000,'https://www.baskinrobbins.co.kr/upload/product/main/aff1c39b1653ddb7701abd9b4c8394ee.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','자모카 아몬드 훠지',5000,'https://www.baskinrobbins.co.kr/upload/product/main/f31388da0371388c2086a7c90990a097.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','초콜릿 칩',5000,'https://www.baskinrobbins.co.kr/upload/product/main/505b2fe8d9c444d638665fbb40c6f8a5.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('초콜릿','아몬드 봉봉',5000,'https://www.baskinrobbins.co.kr/upload/product/main/e7cb5667c3147ddb0b31e28d1f365980.png');
INSERT INTO ICECREAM (CATEGORY, NAME, PRICE, IMG) VALUES ('플레인','바닐라',5000,'https://www.baskinrobbins.co.kr/upload/product/main/901f131644310c0eb356cbab7ecc4738.png');

SELECT * FROM ICECREAM;

# TOPPING DATA INSERTION
INSERT INTO TOPPING (NAME, PRICE, IMG) VALUES ('바닐라', 3000, 'https://royalwholesalecandy.com/cdn/shop/products/817.jpg?height=645&pad_color=fff&v=1682363508&width=645');
INSERT INTO TOPPING (NAME, PRICE, IMG) VALUES ('초콜릿', 3000, 'https://royalwholesalecandy.com/cdn/shop/products/9208.jpg?height=645&pad_color=fff&v=1691429499&width=645');
INSERT INTO TOPPING (NAME, PRICE, IMG) VALUES ('레인보우', 3000, 'https://royalwholesalecandy.com/cdn/shop/products/2713.png?height=240&v=1682357486');

SELECT * FROM TOPPING;

