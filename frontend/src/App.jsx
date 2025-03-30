import React, {useState, useEffect, useRef} from 'react';
import axios from 'axios';
import './index.css'

function Panel() {

    const [msg, setMsg] = useState("");
    const [text, setText] = useState("");

    const txt = useRef(null);

    function handleText(event) {
        setText(event.target.value);
    }

    function handle(id) {
        setMsg({"id": id, "msg": text, "placeholder": `Changing ${id}`});
    }

    function handleSubmit(event) {
        setText("");
        const endpoint = `http://104.39.94.143:5000/${msg.id}/edit`;
        const body = msg.msg;
        axios.post(endpoint, {"message": body})
        .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });;
    }

    useEffect(() => {console.log(msg)}, [msg])

    return (
        <>
        <h1>BAREBONEZ</h1>
        <div className="parent">
            <div className="panel-parent">
                <button className="btn" onClick={() => handle(1)}>1</button>
                <button className="btn" onClick={() => handle(2)}>2</button>
                <button className="btn" onClick={() => handle(3)}>3</button><br />
                <button className="btn" onClick={() => handle(4)}>4</button>
                <button className="btn" onClick={() => handle(5)}>5</button>
                <button className="btn" onClick={() => handle(6)}>6</button><br />
                <button className="btn" onClick={() => handle(7)}>7</button>
                <button className="btn" onClick={() => handle(8)}>8</button>
                <button className="btn" onClick={() => handle(9)}>9</button><br />
                <button className="btn" onClick={() => handle(0)}>0</button>
                <button className="btn submit" onClick={() => handleSubmit()}>Submit</button>
            </div>
            <textarea className="txtarea" ref={txt} onChange={handleText} placeholder={msg.placeholder}/>
        </div>
        </>
    )
}

export default Panel