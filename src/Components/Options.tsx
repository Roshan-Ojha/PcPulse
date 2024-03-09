import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../Miscellaneous/store";
import { add_option } from "../Miscellaneous/optionreducer/optionslice";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faMicrochip,
  faMemory,
  faDatabase,
  faNetworkWired,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";

function Options() {
  const option_list = ["CPU", "Memory", "Disk", "Network"];

  const options = useSelector((state: RootState) => state.option_reducer);

  const dispatch = useDispatch();
  return (
    <>
      {option_list.map((option, key) => (
        <div
          key={key}
          onClick={() => dispatch(add_option(option))}
          className={`p-[10px] m-[40px]  w-[220px] h-[150px] relative border-b-[1px] shadow-md mb-[25px] hover:border-[1px] hover:border-green-700 ${options===option?'border-green-700 border-[3px]':''}  rounded-[20px]`}
        >
          <div className="absolute bottom-[15px] flex flex-col items-center self-center transform -translate-x-1/2 left-1/2">
            <div className="">
              <FontAwesomeIcon
                icon={
                  option === "CPU"
                    ? faMicrochip
                    : option === "Memory"
                    ? faMemory
                    : option === "Disk"
                    ? faDatabase
                    : option === "Network"
                    ? faNetworkWired
                    : faXmark
                }
                style={{
                  height: "75px",
                  width: "75px",
                  background: "transparent",
                  color: "#418CE9",
                }}
              />
            </div>
            <span className="text-[#E05924] text-[20px]">{option}</span>
          </div>
        </div>
      ))}
    </>
  );
}
export default Options;
