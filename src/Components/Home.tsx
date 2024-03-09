import { useState } from "react";
import Pc from "./Pcs";
import SystemInformation from "./SystemInformation";
import Options from "./Options";
function Home() {
  return (
    <div className="flex flex-row justify-around w-full h-full ">
      <div >
        <Options />
      </div>
      <div>
        <SystemInformation />
      </div>
      <div className="border-indigo-500 border-x-[1px]">
        <Pc />
      </div>
    </div>
  );
}
export default Home;
