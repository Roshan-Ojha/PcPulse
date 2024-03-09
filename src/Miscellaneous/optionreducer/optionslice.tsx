import { PayloadAction, createSlice } from "@reduxjs/toolkit";


export const option_slice = createSlice({
    name:'option',
    initialState:"CPU",
    reducers:{
        add_option:(state,action:PayloadAction<string>)=>{
            
            return action.payload
        }
    }
})

export const {add_option} = option_slice.actions

export default option_slice.reducer