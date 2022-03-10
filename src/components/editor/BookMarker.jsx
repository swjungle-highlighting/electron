import React, { useEffect, useState, useRef, useContext } from "react";

import EditorTimePointerContext from "../../contexts/EditorTimePointerContext";
import { format } from "./in_VideoPlayer/Duration";

import "./BookMarker.scss";
import useResult from "../../hooks/useResult";
import "./cardbox.scss";

import BorderColorIcon from "@mui/icons-material/BorderColor";
import DeleteForeverOutlinedIcon from "@mui/icons-material/DeleteForeverOutlined";

function BookMarker({ url, duration, bookmarker }) {
  const {
    pointer,
    callSeekTo,
    setPlayed,
    changePointer,
    seeking,
    setSeeking,
    replayRef,
    fileMp4HtmlRef,
  } = React.useContext(EditorTimePointerContext);
  const [addMarker, setAddMarker] = useState(null);
  const [editingText, setEditingText] = useState("");
  const [isStart, setIsStart] = useState(false);
  const { markers, setMarkers, setRelay, requestExportCut } = useResult();

  const bookscroll = document.querySelector("#bookmarkScroll");


  useEffect(() => {
    const temp = JSON.stringify(markers);
    localStorage.setItem("markers", temp);
  }, [markers]);

  useEffect(() => {
    if (!bookmarker) return;
    setMarkers(bookmarker);
  }, [bookmarker]);

  useEffect(() => {
    if (!replayRef) return;
    replayRef.current.saveMarker = handleClick;
    replayRef.current.cutMarker.doExport = doExport;
  }, [url, markers]);

  const getMarker = () => {
    const selectedMarkers = [...markers].filter(
      (marker) => marker.completed === true
    );
    const cutList = selectedMarkers?.map((marker) => ({
      start: marker.startPointer,
      end: marker.endPointer,
      text: marker.text ? marker.text : 'notitle'
    }));
    return cutList;
  };

  const doExport = async () => {
    if (!fileMp4HtmlRef.current.files[0]){
      return;
    }
    const cutList = getMarker(markers);
    let args = '';
    let i = 0;
    while (i < cutList.length) {
      args += '[cut]';
      args += cutList[i].start;
      args += ' ';
      args += cutList[i].end;
      args += ' ';
      args += cutList[i].text;
      i += 1;
    }
    console.log(fileMp4HtmlRef.current.files[0].path);
    console.log(args);
    requestExportCut(fileMp4HtmlRef.current.files[0].path, args);
  };

  function handleClick(e) {
    if (e) {
      e.preventDefault();
    }
    if (seeking) return;
    console.log(`is replayRef?`, replayRef.current);
    if (replayRef.current.isReplay) {
      const newMarker = {
        id: new Date().getTime(),
        text: "",
        startPointer: replayRef.current.startTime,
        endPointer: replayRef.current.endTime,
        completed: true,
        isPlaying: false,
      };
      setMarkers([...markers].concat(newMarker));
    } else {
      console.log(`isStart`, isStart);
      if (isStart) {
        if (markers.length === 0) {
          setIsStart(false);
        } else {
          const endPointerValue = markers[markers.length - 1];
          endPointerValue["endPointer"] = pointer;
          setIsStart(false);
          console.log(`markers`, markers);
        }
      } else {
        const newMarker = {
          id: new Date().getTime(),
          text: "",
          startPointer: pointer,
          endPointer: null,
          completed: true,
          isPlaying: false,
        };
        setIsStart(true);
        setMarkers([...markers].concat(newMarker));
      }
    }
  }

  function deleteMarker(id) {
    const updateMarkers = [...markers].filter((marker) => marker.id !== id);

    setMarkers(updateMarkers);
  }

  function toggleComplete(id) {
    setSeeking(true);
    const updateMarkers = [...markers].map((marker) => {
      if (marker.id === id) {
        marker.completed = !marker.completed;
      }
      return marker;
    });

    setMarkers(updateMarkers);
    setSeeking(false);
  }

  function addMemoEdit(id) {
    const updateMarkers = [...markers].map((marker) => {
      if (marker.id === id) {
        marker.text = editingText;
      }
      return marker;
    });
    setMarkers(updateMarkers);
    setEditingText("");
    setAddMarker(null);
  }

  function playVideo(id) {
    markers.forEach((marker) => {
      if (marker.id === id) {
        setSeeking(true);
        const playTime = marker.startPointer;
        const playTimeRatio = playTime / parseInt(duration);
        callSeekTo(playTimeRatio);
        setPlayed(parseFloat(playTimeRatio));
        changePointer(playTime);
        setSeeking(false);
        replayRef.current.isReplay = true;
        replayRef.current.startTime = marker.startPointer;
        replayRef.current.endTime = marker.endPointer;
        replayRef.current.playingId = marker.id;
        setRelay((prev) => (prev = true));
      }
    });
  }

  const handleKeyPress = (event, id) => {
    if (event.key === "Enter") {
      console.log("enter press here! ");
      addMemoEdit(id);
    }
  };

  const mounted = useRef([false]);
  useEffect(() => {
    if (!mounted.current) {
      mounted.current = true;
    } else {
      if (markers.length !== 0) {
        bookscroll.lastChild.scrollIntoView();
      }
    }
  }, [markers]);

  return (
    <>
      <div className="BookMarkerContainer">
        <h2>📁 컷 보관함</h2>
        <h3>드래그로 선택한 구간을 컷으로 저장할 수 있어요 (Ctrl+Shift+S)</h3>
        <div className="hello" id="bookmarkScroll">
          {markers.map((marker) => (
            <div key={marker.id}>
              <div className="card">
                <div
                  className="card-header"
                  onClick={(e) => {
                    e.preventDefault();
                    playVideo(marker.id);
                  }}
                >
                  <div
                    className="thumbnail"
                    style={{
                      background: `url(${url?.split("=")[1]}.jpg)`,
                      width: "176px",
                      height: "100px",
                      backgroundRepeat: "no-repeat",
                      backgroundPosition: `  ${
                        -177 *
                          Math.floor(
                            Math.floor(marker.startPointer % 60) / 10
                          ) -
                        1
                      }px  ${-100 * Math.floor(marker.startPointer / 60)}px`,
                    }}
                  />
                </div>
                <div className="card-body">
                  <div className="bookmarkTime">
                    {format(marker.startPointer)}~{format(marker.endPointer)}
                  </div>
                  {addMarker === marker.id ? (
                    <input
                      className="tt"
                      type="text"
                      onKeyPress={(e) => handleKeyPress(e, marker.id)}
                      onChange={(e) => setEditingText(e.target.value)}
                      value={editingText}
                    />
                  ) : marker.text ? (
                    <div className="ttt">{marker.text}</div>
                  ) : (
                    <div className="tt"></div>
                  )}

                  <input
                    className="inputCheckbox"
                    type="checkbox"
                    onChange={() => toggleComplete(marker.id)}
                    checked={marker.completed}
                  />

                  <div className="memoAndDelete">
                    {addMarker === marker.id ? (
                      <button
                        className="saveButton"
                        onClick={() => addMemoEdit(marker.id)}
                      >
                        저장
                      </button>
                    ) : (
                      <BorderColorIcon onClick={() => setAddMarker(marker.id)}>
                        메모
                      </BorderColorIcon>
                    )}
                    <DeleteForeverOutlinedIcon
                      onClick={() => deleteMarker(marker.id)}
                    >
                      삭제
                    </DeleteForeverOutlinedIcon>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default BookMarker;