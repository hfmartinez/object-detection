import "./App.css";
import { useState } from "react";
import axios from "axios";

function App() {
  const [imgPreview, setImage] = useState(null);
  const [Img64, setImage64] = useState(null);

  const onImageChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setImage(URL.createObjectURL(event.target.files[0]));

      var reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);

      reader.onload = () => {
        setImage64(reader.result);
      };
      reader.onerror = (error) => {
        console.log("Error: ", error);
      };
    }
  };
  const onClickProcess = (event) => {
    var regex = /^data:image\/[^;]+;base64,/;
    var base64Data = Img64.replace(regex, "");
    axios
      .post("http://localhost:8000/api/v1/images/", {
        image_base_64: base64Data,
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => console.log(error));
  };
  return (
    <div>
      <h1>Object Detection App</h1>
      <input
        type="file"
        accept="image/*"
        onChange={onImageChange}
        className="filetype"
      />
      <img alt="preview" src={imgPreview} />
      <button onClick={onClickProcess}>process</button>
      <img alt="result" src={Img64} />
    </div>
  );
}

export default App;
