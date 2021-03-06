import React, { useCallback, useState, useRef, useEffect } from "react";
import "./ControllerButtonBox.scss";
import useResult from "../../hooks/useResult";
import EditorTimePointerContext from "../../contexts/EditorTimePointerContext";
import Modal from "../Header/Modal";

const ControllerButtonBox = ({ url, duration }) => {
  const {
    replayRef,
    pointer,
    isplaying,
    setIsplaying,
    setSeeking,
    callSeekTo,
    setPlayed,
    changePointer,
    setFileMp4HtmlRef,
  } = React.useContext(EditorTimePointerContext);
  const {
    requestKeywordsData,
    isChatSuper,
    setIsChatSuper,
    isChatKeywords,
    setIsChatKeywords,
  } = useResult();

  const [keywords, setKeywords] = useState("");
  const isTypingRef = useRef(false);

  // 내보내기 관련
  const fileMp4Html = useRef(null);
  const [modalOpen, setModalOpen] = useState(false);
  // const [outName, setOutName] = useState("");

  useEffect(() => {
    if (!fileMp4Html) return;
    setFileMp4HtmlRef(fileMp4Html);
  }, [fileMp4Html])

  // 모달창
  const openModal = () => {
    document.body.style.overflow = "hidden";
    setModalOpen(true);
  };
  const closeModal = () => {
    document.body.style.overflow = "unset";
    setModalOpen(false);
  };

  // 슈퍼챗 버튼 이벤트
  function handleIsChatSuper() {
    if (isChatSuper === -1) setIsChatSuper(false);
    else {
      setIsChatSuper((prev) => !prev);
    }
  }

  function handleIsChatKeywords() {
    // isChatKeywords ? 닫힌상태 : 열린상태
    if (isChatKeywords === -1) {
      setIsChatKeywords((prev) => prev + 1);
    } else {
      setIsChatKeywords((prev) => (prev ? 0 : prev + 1));
    }
  }

  const onChangeInput = useCallback((e) => {
    console.log("onChangeInput");
    isTypingRef.current = true;
    const tmpKeywords = e.target.value;
    setKeywords(tmpKeywords);
  }, []);

  const keywordSearchEvent = () => {
    if (keywords === "") {
      alert("검색 키워드를 입력해주세요!!");
    } else {
      console.log("url", url, "keywords", keywords);
      requestKeywordsData(url, keywords);
    }
  };

  // 좌우 화살표 키 누를 때 이동 시간(초)
  const ARROW_MOVING_TIME = 5;
  // 좌, 우 화살표 재생 이동 함수
  function arrowPlayBarMove(direction, padding = 10) {
    setSeeking(true);
    let playTime;
    if (direction === "LEFT") {
      playTime = pointer - padding;
    } else if (direction === "RIGHT") {
      playTime = pointer + padding;
    } else {
      return;
    }
    let playTimeRatio = playTime / duration;
    callSeekTo(playTimeRatio);
    setPlayed(parseFloat(playTimeRatio));
    changePointer(playTime);
    setSeeking(false);
  }

  // window Keydown event
  useEffect(() => {
    const handleKeyboardDown = (event) => {
      if (!isTypingRef.current) {
        const keyCode = event.code;
        switch (keyCode) {
          case "Space":
            console.log("sapce실행", isTypingRef.current);
            if (isTypingRef.current) return;
            setIsplaying(!isplaying);
            return;
          case "ArrowLeft":
            arrowPlayBarMove("LEFT", ARROW_MOVING_TIME);
            return;
          case "ArrowRight":
            arrowPlayBarMove("RIGHT", ARROW_MOVING_TIME);
            return;
          case "ShiftLeft":
            replayRef.current.subKey.isShiftKey = true;
            return;
          case "ControlLeft":
            replayRef.current.subKey.isCtrlKey = true;
            return;
          case "KeyS":
            if (
              replayRef.current.subKey.isShiftKey &&
              replayRef.current.subKey.isCtrlKey
            ) {
              replayRef.current.saveMarker();
            }
            replayRef.current.wordKey.isS = true;
            return;
          default:
            return;
        }
      }
    };
    window.addEventListener("keydown", handleKeyboardDown);
    return () => {
      window.removeEventListener("keydown", handleKeyboardDown);
    };
  }, [url, pointer, isplaying, isChatKeywords]);

  // window Keyup event
  useEffect(() => {
    const handleKeyboardUp = (event) => {
      if (!isTypingRef.current) {
        const keyCode = event.code;
        switch (keyCode) {
          case "Space":
            break;
          case "ShiftLeft":
            replayRef.current.subKey.isShiftKey = false;
            break;
          case "ControlLeft":
            replayRef.current.subKey.isCtrlKey = false;
            break;
          case "KeyS":
            replayRef.current.wordKey.isS = false;
            break;
          case "ArrowLeft":
            break;
          case "ArrowRight":
            break;
          default:
            return;
        }
      }
    };
    window.addEventListener("keyup", handleKeyboardUp);
    return () => {
      window.removeEventListener("keyup", handleKeyboardUp);
    };
  }, [url, pointer, isplaying, isChatKeywords]);

  return (
    <div className="buttonContainer">
      <button
        className="superchat"
        onClick={handleIsChatSuper}
        value={isChatSuper}
      >
        {isChatSuper ? (
          <span className="ON">슈퍼챗</span>
        ) : (
          <span className="OFF">슈퍼챗 </span>
        )}
      </button>
      {isChatKeywords ? (
        <button className="keyWordStart">
          <span onClick={handleIsChatKeywords}>키워드 검색</span>
        </button>
      ) : (
        <button className="keyWordEnd">
          <span onClick={handleIsChatKeywords}>검색종료</span>
        </button>
      )}

      {/* 인풋창~검색 */}
      {!isChatKeywords ? (
        <div className="inputSearchContainer">
          <input
            className="InputBar"
            placeholder="키워드 입력"
            onChange={onChangeInput}
            value={keywords}
            onFocus={() => {
              isTypingRef.current = true;
            }}
            onBlur={() => {
              isTypingRef.current = false;
            }}
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                keywordSearchEvent();
              }
            }}
          />
          <button className="Search">
            <span onClick={keywordSearchEvent}>검색</span>
          </button>
        </div>
      ) : (
        ""
      )}
      {/* 인풋창~검색 */}
      <button
        className="cutMakeButton"
        onClick={replayRef?.current ? replayRef.current.saveMarker : null}
      >
        <span>컷 만들기</span>
      </button>
      <button className="exportButton" onClick={openModal}>
        <span>내보내기</span>
      </button>
      {modalOpen && (
        <Modal
          // ref={modalEl}
          open={modalOpen}
          close={closeModal}
          Header="내보내기"
        >
          <p>
            {replayRef?.current ? replayRef.current.cutMarker.message : null}
          </p>
          <input ref={fileMp4Html} id="mp4" type="file" accept=".mp4" />
          <button
            onClick={
              replayRef?.current ? replayRef.current.cutMarker.doExport : null
            }
          >
            Start
          </button>
        </Modal>
      )}

    </div>
  );
};

export default ControllerButtonBox;