import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import BounceLoader from "react-spinners/ClipLoader";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Line,
  ResponsiveContainer,
} from "recharts";

import { RootState } from "../Miscellaneous/store";

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{ payload: { x: string; y: number } }>;
}

interface IpState {
  ip: string;
}

interface ChartData {
  x: string;
  y: string;
}

function SystemInformation() {
  const ip = useSelector((state: RootState) => state.ip_reducer); //This ip reducer is used to define slice in store
  const option = useSelector((state: RootState) => state.option_reducer);
  const mode = useSelector((state:RootState)=>state.toogle_reducer)

  const [system_data, set_sysetm_data] = useState<Record<string, any>>({}); //Record<string, any> is a generic type from TypeScript that represents an object where:
  // string is the type of the object's keys (always strings in this case).
  // any is the type of the object's values (meaning they can be any data type).
  const [storage_chartdata, setstorage_chartdata] = useState(
    Array.from({ length: 10 }, () => ({ x: 0, y: 0 }))
  );
  const [memory_chartdata, setmemory_chartdata] = useState(
    Array.from({ length: 10 }, () => ({ x: 0, y: 0 }))
  );
  const [cpu_chartdata, setcpu_chartdata] = useState(
    Array.from({ length: 10 }, () => ({ x: 0, y: 0 }))
  );
  const [network_chartdata, setnetwork_chartdata] = useState(
    Array.from({ length: 10 }, () => ({ x: 0, y: 0 }))
  );

  useEffect(() => {
    
    const web_socket_url = `ws://127.0.0.1:8000/ws/system_info/?ip=${ip.ip}`
    
    const ws = new WebSocket(web_socket_url);
    ws.onopen = () => {
      console.log(web_socket_url)
      console.log("websocket connected");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      //   set_sysetm_data(data);
     
      const {
        total_storage,
        used_storage,
        free_storage,
        total_memory,
        used_memory,
        free_memory,
        uptime,
        cpu_usage,
        upload,
        download,
        time,
      } = data;

      console.log("data", data)
      switch (option) {
        case "Disk":
          set_sysetm_data({
            total_storage,
            used_storage,
            free_storage,
            time,
          });
          setstorage_chartdata((prev_data) => [
            ...prev_data.slice(-9),
            { x: time, y: used_storage },
          ]);
          break;
        case "Memory":
          set_sysetm_data({
            total_memory,
            used_memory,
            free_memory,
            time,
          });
          setmemory_chartdata((prev_data) => [
            ...prev_data.slice(-9),
            { x: time, y: used_memory },
          ]);
          break;
        case "CPU":
          set_sysetm_data({
            uptime,
            cpu_usage,
            time,
          });
          setcpu_chartdata((prev_data) => [
            ...prev_data.slice(-9),
            { x: time, y: cpu_usage },
          ]);
          break;
        case "Network":
          set_sysetm_data({
            upload,
            download,
            time,
          });
          setnetwork_chartdata((prev_data) => [
            ...prev_data.slice(-9), // Keep the most recent 9 elements
            { x: time, y: download },
          ]);
          break;
        default:
          return "Invalid";
      }
      // console.log(storage_chartdata)
      
    };

    ws.onclose = () => {
      console.log("Connection closed");
    };

    return () => {
      ws.close(); // Close the WebSocket connection when component unmounts
    };
   
  }, [ip.ip, option]);

  // console.log("system",system_data)
  // console.log("cpu",cpu_chartdata)

  const CustomTooltipContent: React.FC<CustomTooltipProps> = ({
    active,
    payload,
  }) => {
    if (active && payload && payload.length) {
      const data = payload[0];

      return (
        <div
          style={{
            background: "white",
            border: "1px solid #ccc",
            padding: "10px",
          }}
        >
          <p>{`Time: ${data.payload.x}`}</p>
          <p>{`${
            option === "Disk"
              ? "Used Disk: "
              : option === "Memory"
              ? "Used Memory: "
              : option === "CPU"
              ? "Used CPU: "
              : option === "Network"
              ? "Download Speed: "
              : "Nothing"
          }: ${data.payload.y}`}</p>
          {/* Add more data points as needed */}
        </div>
      );
    }
  };

  return (
    <div className="flex flex-col items-center justify-center mt-[40px]">
      {/* <div>Hello</div>
      <div>{ip.ip}</div>
      <div>{option}</div> */}

      <AreaChart
        width={1000}
        height={800}
        data={
          option === "Disk"
            ? storage_chartdata
            : option === "Memory"
            ? memory_chartdata
            : option === "CPU"
            ? cpu_chartdata
            : option === "Network"
            ? network_chartdata
            : [{ error: true }]
        }
        margin={{
          top: 10,
          right: 30,
          left: 0,
          bottom: 0,
        }}
      >
        <CartesianGrid />
        <XAxis dataKey={"x"} />
        <YAxis />
        <Tooltip content={<CustomTooltipContent />} />
        <Area type="monotone" dataKey="y" stroke="#8884d8" fill="#8884d8" />
        {/* {option==="network"&&<Line type="monotone" dataKey="z" stroke="black"/>} */}
      </AreaChart>
      <div className="w-[80%]  p-[20px]">
        {Object.entries(system_data).map(([key, value]) => (
          <div key={key} className=" text-[30px]">
           
              <span className="text-[#7b7f32] font-bold">
                {key === "uptime"
                  ? "Uptime"
                  : key === "cpu_usage"
                  ? "CPU Usage"
                  : key === "time"
                  ? "Time"
                  : key === "total_memory"
                  ? "Total Memory"
                  : key === "used_memory"
                  ? "Used Memory"
                  : key === "free_memory"
                  ? "Free Memory"
                  : key === "total_storage"
                  ? "Total Storage"
                  : key === "used_storage"
                  ? "Used Storage"
                  : key === "free_storage"
                  ? "Free Storage"
                  : key === "upload"
                  ? "Upload Speed"
                  : key == "download"
                  ? "Download Speed"
                  : key}
                :{" "}
              </span>&nbsp;
              <span className={`${!mode?'text-[#bfdccb]':'text-[#242424]'}`}>
              {!value && <BounceLoader color="#36d7b7" />}
              {value}{" "}
              {key === "cpu_usage"
                ? "%"
                : key == "total_memory" ||
                  key == "used_memory" ||
                  key == "free_memory"
                ? "MB"
                : key == "total_storage" ||
                  key == "free_storage" ||
                  key == "used_storage"
                ? "GB"
                : key == "upload" ||
                key == "download" 
                ? "KB/S"
                : ""}
                </span>
            </div>
          
        ))}
      </div>
      {/* <div>
        <div>{system_data.total_storage}</div>
        <div>{system_data.used_storage}</div>
        <div>{system_data.free_storage}</div>
        <div>{system_data.total_memory}</div>
        <div>{system_data.used_memory}</div>
        <div>{system_data.free_memory}</div>
        <div>{system_data.uptime}</div>
        <div>{system_data.cpu_usage}</div>
        <div>{system_data.upload}</div>
        <div>{system_data.download}</div>
        <div>{system_data.time}</div>
        <br></br>
      </div> */}

      {/* {
        system_data.map((element,key)=>(
            <div key={key}>
            <div>{element.total_storage}</div>
            <div>{element.used_storage}</div>
            <div>{element.free_storage}</div>
            <div>{element.total_memory}</div>
            <div>{element.used_memory}</div>
            <div>{element.free_memory}</div>
            <div>{element.uptime}</div>
            <div>{element.cpu_usage}</div>
            <div>{element.upload}</div>
            <div>{element.download}</div>
            <div>{element.time}</div>
            <br></br>

            
            </div>
        ))
    } */}
    </div>
  );
}
export default SystemInformation;
