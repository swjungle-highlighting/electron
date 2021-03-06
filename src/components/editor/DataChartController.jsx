import { useState, useEffect } from "react";
import useResult from "../../hooks/useResult";
import "./DataChartController.scss";

function DataChartController() {
  const { isChatKeywords } = useResult();
  const [test, setTest] = useState("container__chat");

  useEffect(() => {
    console.log(isChatKeywords);
    setTest("");
    setTimeout(() => setTest("container__chat"), 0.01);
  }, [isChatKeywords]);

  return (
    <>
      {isChatKeywords ? (
        <div className={test}>
        <h2 className="header"> μ±ν λΉλ π¬ </h2>
          <h3 className="content">λμμλ‘ μμ²­μ λ°μμ΄ μ’μ μ₯λ©΄μ΄μμ</h3>
        </div>
      ) : (
        <div className={test}>
          <h2 className="header"> ν€μλ κ°μ§ π­ </h2>
          <h3 className="content">
            κ²μν ν€μλκ° μΌλ§λ λ±μ₯νλμ§ λ³΄μ¬μ€μ
          </h3>
        </div>
      )}
      <div className="container__video">
      <h2 className="header"> νλ©΄ λ³ν π₯</h2>
        <h3 className="content">λΎ°μ‘±ν λΆλΆμ΄ μ₯λ©΄μ΄ λ°λλ μκ°μ΄μμ</h3>
      </div>
      <div className="container__audio">
      <h2 className="header"> μ€λμ€ λ³Όλ₯¨ π</h2>
        <h3 className="content">λκΊΌμ°λ©΄ μλλ½κ³ , μμΌλ©΄ μ‘°μ©ν μ₯λ©΄μ΄μμ</h3>
      </div>
    </>
  );
}

export default DataChartController;