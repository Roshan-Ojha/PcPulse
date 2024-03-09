import Home from "./Components/Home";
import { toogle } from "./Miscellaneous/tooglereducer/toogleslice";
import {  useDispatch, useSelector } from "react-redux";
import { RootState } from "./Miscellaneous/store";
import './App.css'

function App() {
  const toogle_mode = useDispatch()
  const mode = useSelector((state:RootState)=>state.toogle_reducer)
  console.log("mode",mode)
  return (
    <>

     <div className={`min-h-screen ${mode==true?"":"bg-[#242424]"} flex flex-col `}>
     <label className="self-center switch mt-[20px]">
     <input type="checkbox" onChange={(e) =>toogle_mode(toogle())} checked={!mode} />
        <span className="slider"></span>
      </label>
       <Home/>
     </div>
    </>
  );
}

export default App;
