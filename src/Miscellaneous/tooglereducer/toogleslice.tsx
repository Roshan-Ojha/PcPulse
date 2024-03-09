import { createSlice } from "@reduxjs/toolkit";

export const toogle_slice = createSlice({
    name:'theme_toogle',
    initialState:true,
    reducers:{
        toogle:(state)=>{
            state = !state
            return state
        }
    }
})

export const {toogle} = toogle_slice.actions

export default toogle_slice.reducer