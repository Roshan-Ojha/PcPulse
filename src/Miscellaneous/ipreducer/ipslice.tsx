import  {createSlice, nanoid, PayloadAction} from '@reduxjs/toolkit'

interface IpState{
    ip:string;
}

const initial_ip:IpState= {
    ip:"" 
}

export const ip_slice = createSlice({
    name:'ip_slice_name',
    initialState:initial_ip,
    reducers:{
        add_ip:(state,action: PayloadAction<string>)=>{
            // const ip_address ={
            //     ip: action.payload.ip
            // }
            state.ip = action.payload
    
        },
    }
})

export const {add_ip} = ip_slice.actions   //Export functionalities like add_ip. We would always update state through it
// export  const ip_slice.actions.add_ip

export default ip_slice.reducer //export all reducer to aware the Store about all the avilable reducers. Otherwise it cannot manage store