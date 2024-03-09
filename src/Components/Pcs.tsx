import { useEffect, useState } from "react";

import { add_ip } from "../Miscellaneous/ipreducer/ipslice";
import { useDispatch, useSelector } from "react-redux";

import { RootState } from "../Miscellaneous/store";

function Pc() {
  //Dispatch changes the values in store using reducer

  const [PCinfo, SetPCinfo] = useState<any[]>([]);
  const dispatch = useDispatch();
  const mode = useSelector((state:RootState)=>state.toogle_reducer)

  

  const ip = useSelector((state: RootState) => state.ip_reducer);

  // useEffect hook in React's TypeScript integration expects the first argument to be a callback function
  // that either returns void (nothing) or a function for cleanup.
  useEffect(() => {
    const fetchdata = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/pcinfo/");
        const data = await response.json();
        SetPCinfo(data.data);
      } catch (error) {
        console.log("Error", error);
      }
    };
    fetchdata();
  }, []);

  return (
    <>
      {PCinfo?.map((element, index) => (
        <div
          className={`p-[10px] m-[40px] border-[1px] ${
            ip.ip === element.ip ? "border-green-600" : "border-gray-700"
          } w-[250px] h-[200px] bg-black bg-opacity-30 rounded-[20px] flex flex-col`}
          key={index}
          onClick={() => dispatch(add_ip(element.ip))}
        >
          <div className="self-center text-white text-[30px] mb-[20px]">
            <span className={`font-bold ${!mode?'text-[#bfdccb]':'text-[#242424]'} `}>User: </span>
            {element.username}
          </div>
          <div className=" text-[#149414] text-[20px]">
            <span className="font-bold">Ip: </span>
            {element.ip}
          </div>
          <div className="text-[#E05924] text-[20px]">
            <span className="font-bold">Host: </span>
            {element.hostname}
          </div>
        </div>
      ))}
    </>
  );
}
export default Pc;
