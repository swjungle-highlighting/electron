import React, { useState, useRef, useCallback } from "react";

import useResult from "../hooks/useResult";
import useRoute from "../hooks/useRoute";
import Header from "../components/Header/Header";
import { GiPlayButton } from "react-icons/gi";
import { AiOutlineSearch } from "react-icons/ai";
import "./Home.scss";

const Home = () => {
  const inputValue = document.getElementById("link");
  const urlInput = useRef();

  const { logged, onLogout } = useResult();
  const { url, setUrl } = useResult();
  const { requestResult } = useRoute();
  const [active0, setActive0] = useState(true);
  const [active1, setActive1] = useState(false);
  const [active2, setActive2] = useState(false);
  const [active3, setActive3] = useState(false);

  const onChangeUrl = useCallback((e) => {
    const value = e.target.value;
    console.log(value);
    setUrl(value);
  });

  function linkCheck() {
    console.log(url);
    if (!url) {
      alert("빈 값입니다. 입력창에 유튜브 주소를 입력해 주세요.");
      focusUrl();
      return;
    }
    else {
      const isYT = url.substr(0, 32) === "https://www.youtube.com/watch?v=";
      const isTW = url.substr(0, 29) === "https://www.twitch.tv/videos/";

      if (isYT) {
        requestResult(url.substr(0, 43));
        setUrl(url.substr(0, 43));
        return;
      }
      if (isTW) {
        requestResult(url.substr(0, 39));
        setUrl(url.substr(0, 39));       
        return;
      }
      alert("올바른 주소가 아닙니다. 유튜브, 트위치 다시보기 링크를 입력해 주세요.");
      focusUrl();
    }
  }

  function focusUrl() {
    if (inputValue === null) return;
    inputValue.value = "";
    urlInput.current.focus();
  }

  const onClickGuide = (e) => {
    const id = e.target.id;
    switch (id) {
      case "zero":
        activeZero();
        break;
      case "first":
        activeFirst();
        break;
      case "second":
        activeSecond();
        break;
      case "third":
        activeThird();
        break;
      default:
    }
  };

  const viewChange = () => {
    document.getElementById("guidline").scrollIntoView({ behavior: "smooth" });
  };
  const activeZero = () => {
    setActive0(true);
    setActive1(false);
    setActive2(false);
    setActive3(false);
  };

  const activeFirst = () => {
    setActive0(false);
    setActive1(true);
    setActive2(false);
    setActive3(false);
  };

  const activeSecond = () => {
    setActive0(false);
    setActive1(false);
    setActive2(true);
    setActive3(false);
  };

  const activeThird = () => {
    setActive0(false);
    setActive1(false);
    setActive2(false);
    setActive3(true);
  };

  return (
    <div>
      <Header logged={logged} onLogout={onLogout} />
      <div className="HomeContainer">
        <div className="UpperContainer">
          <div className="upper_left_container">
          </div>
          <div className="upper_right_container">
            <div className="Home_urlInput">
            <h1> <img className="inputLogo" src="Logo.png" alt="Logo" onClick={linkCheck} />HIGHLIGHTING </h1>
              <AiOutlineSearch className="test" />
              <input
                className="InputBar"
                ref={urlInput}
                placeholder="스트리밍 다시보기 영상 URL을 입력해주세요"
                onChange={onChangeUrl}
                id="link"
                onKeyPress={(e) => {
                  if (e.key === "Enter") {
                    linkCheck();
                  }
                }}
                autocomplete="off"
              />
              <h3>
                ⚠ 채팅 내역이 존재하는{" "}
                <span className="point" onClick={viewChange}>
                  다시보기 스트리밍 영상
                </span>{" "}
                이 아니면 분석이 어렵습니다.
              </h3>

              <button className="resultButton" onClick={linkCheck}>
                <span>분석 시작!</span>
              </button>
              <p className="HC1-p4">
                Creating and Providing Services :{" "}
                <span className="point1">Team HIGHLIGHTING</span>
              </p>
            </div>
            {/* 우상단 URL 입력창 */}
          </div>
        </div>

        <div className="LowerContainer">
          <div className="lower_left_container">
            {/* 좌하단 가이드라인 */}
            <div className="Home_introduction_heading_wrap">
              <h2 id="guidline"> 단계별 가이드라인 </h2>
            </div>
            <ul className="Home_list">
              <li className="Home_list-item">
                <div>
                  <p
                    className={
                      "Home_list-content" + " " + (active0 ? "is-active" : "")
                    }
                    id="zero"
                    onMouseEnter={onClickGuide}
                  >
                    0 - 다시보기 스트리밍 영상이란?
                  </p>
                  <p
                    className={
                      "Home_list-sub" + " " + (active0 ? "sub-active" : "")
                    }
                  >
                    다시보기 스트리밍 영상이란 다음의 영상들을 의미합니다. 해당
                    영상링크가 아닐 경우 분석이 불가능합니다.
                  </p>
                </div>
              </li>

              <li className="Home_list-item">
                <div className="Home_list-content-wrap">
                  <p
                    className={
                      "Home_list-content" + " " + (active1 ? "is-active" : "")
                    }
                    id="first"
                    onMouseEnter={onClickGuide}
                  >
                    1 - 키보드 조작방법
                  </p>
                  <p
                    className={
                      "Home_list-sub" + " " + (active1 ? "sub-active" : "")
                    }
                  >
                    저희 HIGHLIGHTING은 다양한 키보드 단축키들을 제공합니다.
                  </p>
                </div>
              </li>

              <li className="Home_list-item">
                <div className="Home_list-item-image"></div>
                <div className="Home_list-content-wrap">
                  <p
                    className={
                      "Home_list-content" + " " + (active2 ? "is-active" : "")
                    }
                    id="second"
                    onMouseEnter={onClickGuide}
                  >
                    2 - 키워드 검색 기능
                  </p>
                  <p
                    className={
                      "Home_list-sub" + " " + (active2 ? "sub-active" : "")
                    }
                  >
                    내가 원하는 키워드의 사용 빈도와 도네이션의 발생 시점등을
                    알려줍니다.
                  </p>
                </div>
              </li>

              <li className="Home_list-item">
                <div className="Home_list-content-wrap">
                  <p
                    className={
                      "Home_list-content" + " " + (active3 ? "is-active" : "")
                    }
                    id="third"
                    onMouseEnter={onClickGuide}
                  >
                    3단계 - 북마크 기능
                  </p>
                  <p
                    className={
                      "Home_list-sub" + " " + (active3 ? "sub-active" : "")
                    }
                  >
                    원하는 구간을 컷으로 편집하여 보관, 저장하여 다시 볼 수
                    있습니다.
                  </p>
                  <a className="UPscroll">
                    <br />
                    <br />
                    <br />
                    <span
                      className="point2"
                      onClick={() => {
                        document
                          .getElementById("Home")
                          .scrollIntoView({ behavior: "smooth" });
                      }}
                    >
                      상단
                    </span>
                    으로 돌아가기
                  </a>
                </div>
              </li>
            </ul>
            {/* 좌하단 가이드라인 */}
          </div>
          <div className="lower_right_container">
            {/* 우하단 내용 컨테이너 */}
            <div className="Home_GuidelineContainer" id="guideContainer">
              {active0 ? (
                <div className="GuideLine_content">
                  <h2>다시보기 영상이란?</h2>
                  <div className="guide_content_box">
                    <img className="review1" src="re1.png" alt = "step" />
                    <p className="guide_content_p1">
                      1. 동영상 - 필터 - 지난 방송 탭의 영상
                    </p>
                    <img className="review2" src="re2.png" alt = "step" />

                    <p className="guide_content_p2">
                      2. 이전 실시간 스트림 탭의 영상
                    </p>
                  </div>
                  <div className="guide_button_box">
                    <GiPlayButton
                      className="previousButton"
                      onClick={() => {
                        activeThird();
                        viewChange();
                      }}
                    />{" "}
                    <GiPlayButton
                      className="nextButton"
                      onClick={() => {
                        activeFirst();
                        viewChange();
                      }}
                    />
                  </div>
                </div>
              ) : (
                ""
              )}
              {active1 ? (
                <div className="GuideLine_content">
                  <h2> 키보드 조작 방법</h2>
                  <div className="guide_content_box">
                  <img className="review3" src="bg.png" alt = "step" />
                    <p className="guide_content_p1">1. space바 : 재생 / 정지</p>
                    <p className="guide_content_p1">
                      2. 좌(◀), 우(▶) 버튼 : 5초 단위 앞, 뒤로 영상 시점 이동
                    </p>
                    <p className="guide_content_p1">
                      3. Ctrl + shift + S : 마우스 드래그한 범위 컷편집 저장
                    </p>
                  </div>
                  <div className="guide_button_box">
                    <GiPlayButton
                      className="previousButton"
                      onClick={() => {
                        activeZero();
                        viewChange();
                      }}
                    />{" "}
                    <GiPlayButton
                      className="nextButton"
                      onClick={() => {
                        activeSecond();
                        viewChange();
                      }}
                    />
                  </div>
                </div>
              ) : (
                ""
              )}
              {active2 ? (
                <div className="GuideLine_content">
                  <h2>키워드 검색 기능</h2>
                  <div className="guide_content_box">
                  <img className="review1" src="p1.png" alt = "step" />
                    <p className="guide_content_p1">
                      {" "}
                      키워드 검색 버튼 클릭후 키워드 입력
                    </p>
                    <img className="review2" src="re2.png" alt = "step" />
                    <p className="guide_content_p2">
                      {" "}
                      키워드 입력 후 검색버튼 활성화 시 차트 데이터 변경
                    </p>
                  </div>
                  <div className="guide_button_box">
                    <GiPlayButton
                      className="previousButton"
                      onClick={() => {
                        activeFirst();
                        viewChange();
                      }}
                    />{" "}
                    <GiPlayButton
                      className="nextButton"
                      onClick={() => {
                        activeThird();
                        viewChange();
                      }}
                    />
                  </div>
                </div>
              ) : (
                ""
              )}
              {active3 ? (
                <div className="GuideLine_content">
                  <h2>북마크 기능</h2>
                  <div className="guide_content_box">
                  <img className="review1" src="p4.png" alt = "step" />
                    <p className="guide_content_p1">
                      차트에서 원하는 영역 드래그
                    </p>
                    <img className="review2" src="p5.png" alt = "step" />
                    <p className="guide_content_p2">
                      컷 만들기 버튼을 누르거나 단축키(ctrl+shift+S) 입력 시 컷
                      저장
                    </p>
                  </div>
                  <div className="guide_button_box">
                    <GiPlayButton
                      className="previousButton"
                      onClick={activeSecond}
                    />{" "}
                    <GiPlayButton className="nextButton" onClick={activeZero} />
                  </div>
                </div>
              ) : (
                ""
              )}
            </div>
            {/* 우하단 내용 컨테이너 */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;