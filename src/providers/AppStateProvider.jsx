import { useState } from "react";
import AppStateContext from "../contexts/AppStateContext";
import { useHistory } from "react-router-dom";

const electron = window.require('electron');
const { ipcRenderer } = electron;


const AppStateProvider = ({ children }) => {
  const [url, setUrl] = useState();
  const [audio, setAudio] = useState();
  const [video, setVideo] = useState();
  const [duration, setDuration] = useState();
  const [chatDistribution, setChatDistribution] = useState();
  const [chatSet, setChatSet] = useState();
  const [chatSuper, setChatSuper] = useState();
  const [chatKeywords, setChatKeywords] = useState();
  const [isChatSuper, setIsChatSuper] = useState(-1);
  const [isChatKeywords, setIsChatKeywords] = useState(-1);
  const [isKeywordsDownload, setIsKeywordsDownload] = useState(0);
  const [title, setTitle] = useState();
  const [thumbnail, setThumNail] = useState();
  const [bookmarker, setBookmarker] = useState();
  const [markers, setMarkers] = useState([]);
  const [relay, setRelay] = useState(false);
  const [receivedDataSetList, setReceivedDataSetList] = useState();
  const [logged, setLogged] = useState(false);

  const history = useHistory();
  const goEditor = () => {
    history.push("/editor");
  };

  const goLoading = () => {
    history.push("/loading");
  };

  const goNotFound = () => {
    history.push("/notfound");
  };

  function requestResult(url) {
    ipcRenderer.on('toApp : process result [stream analysis]', (event, args) => {
      console.log(args)
      try{
        let data = JSON.parse(args)
        localStorage.setItem("localDuration", data.duration);
        setDuration(data.duration);
        localStorage.setItem("prevUrl", url);
        localStorage.setItem(
          "markers",
          JSON.stringify(data.bookmarker)
        );
        setBookmarker(data.bookmarker);
        localStorage.setItem("localAudio", data.audio);
        setAudio(data.audio);
        localStorage.setItem(
          "localChatDistribution",
          data.chat[0]
        );
        setChatDistribution(data.chat[0]);
        localStorage.setItem(
          "localChatSet",
          JSON.stringify(data.chat[1])
        );
        setChatSet(data.chat[1]);
        localStorage.setItem("localChatSuper", data.chat[2]);
        setChatSuper(data.chat[2]);
        localStorage.setItem("localVideo", data.video);
        setVideo(data.video);
        const title = data.title;
        setTitle(title);
        const thumbnail = data.thumbnail;
        setThumNail(thumbnail);
        goEditor();

      }catch(e){
        console.log(e)
      }
  	});
    ipcRenderer.send('toElectron : process call [stream analysis]', {
  		url: url,
  	});
    goLoading();
  }

  function requestKeywordsData(url, keywords) {
    ipcRenderer.once('toApp : process result [keywords search]', (event, args) => {
      let data = JSON.parse(args)
      const objChatKeywords = data.result.distribution.map(
        (value, index) => ({ x: index, y: value })
      );
      setChatKeywords(objChatKeywords);
      setIsKeywordsDownload((prev) => prev + 1);
  	});
    ipcRenderer.send('toElectron : process call [keywords search]', {
  		url: url,
      keywords: keywords,
  	});
  }

  function requestExportCut(file, cuts) {
    console.log("cuts export start");
    ipcRenderer.on('toApp : process result [cuts export]', (event, args) => {
      console.log(args);
  	});
    ipcRenderer.send('toElectron : process call [cuts export]', {
  		file: file,
      cuts: cuts,
  	});
  }



  function onLogin() {
    setLogged(true);
  }

  const onLogout = () => {
    setLogged(false);
    history.push("/");
  };

  function mapValueToObj(raw) {
    return raw.map((value, index) => ({ name: index, value: value }));
  }

  return (
    <AppStateContext.Provider
      value={{
        relay,
        markers,
        bookmarker,
        url,
        audio,
        video,
        duration,
        chatDistribution,
        chatSet,
        chatSuper,
        chatKeywords,
        isChatSuper,
        isChatKeywords,
        isKeywordsDownload,
        receivedDataSetList,
        title,
        thumbnail,
        logged,
        setLogged,
        setTitle,
        setThumNail,

        setRelay,
        setMarkers,
        setBookmarker,
        setUrl,
        setAudio,
        setVideo,
        setDuration,
        setChatDistribution,
        setChatSet,
        setChatSuper,
        setIsChatSuper,
        setChatKeywords,
        setIsChatKeywords,
        setIsKeywordsDownload,
        setReceivedDataSetList,

        mapValueToObj,
        onLogin,
        onLogout,
        requestKeywordsData,
        requestResult,
        requestExportCut,
        goEditor,
        goLoading,
        goNotFound,
      }}
    >
      {children}
    </AppStateContext.Provider>
  );
};

export default AppStateProvider;
