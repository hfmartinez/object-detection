import "./App.css";
import { useState } from "react";
import { useEffect } from "react";
import axios from "axios";
import Select from "react-select";

function App() {
  const [imgPreview, setImage] = useState(null);
  const [img64, setImage64] = useState(null);
  const [filtersIsActive, setActivateFilters] = useState(false);
  const [loader, setLoader] = useState(false);
  const [imgId, setImgId] = useState(null);
  const [newImg64, setNewImg64] = useState(null);
  const [confidence, setConfidence] = useState(0.5);
  const [labelSearch, setLabelSearch] = useState("");
  const [labels, setLabels] = useState([]);

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
  const onClickProcess = async () => {
    var regex = /^data:image\/[^;]+;base64,/;
    var base64Data = img64.replace(regex, "");
    setActivateFilters(false);
    setLoader(true);
    try {
      var response = await axios.post("http://localhost:8000/api/v1/images/", {
        image_base_64: base64Data,
      });

      if (response.status === 200) {
        setImgId(response.data.id);
        response = await axios.get(
          `http://localhost:8000/api/v1/boxes/${response.data.id}`,
          {
            params: {
              label: labelSearch,
              confidence: confidence,
            },
          }
        );
        if (response.status === 200) {
          setNewImg64(response.data.new_image_base_64);
        }
        setLoader(false);
        setActivateFilters(true);
      }
    } catch (error) {
      console.log(error);
    }
  };
  const onClickFilter = () => {
    console.log(labelSearch);
    axios
      .get(`http://localhost:8000/api/v1/boxes/${imgId}`, {
        params: {
          label: labelSearch.value,
          confidence: confidence,
        },
      })
      .then((response) => {
        if (response.status === 200) {
          setNewImg64(response.data.new_image_base_64);
        }
      })
      .catch((error) => console.log(error));
  };
  useEffect(() => {
    async function fetchData() {
      var response = await axios.get("http://localhost:8000/api/v1/classes/");
      if (response.status === 200) {
        setLabels(
          response.data.map((x) => {
            return { value: x, label: x };
          })
        );
      }
    }
    fetchData();
  }, []);
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
      <img alt="result" src={`data:image/png;base64,${newImg64}`} />
      {loader && <div>Set loader</div>}
      {filtersIsActive && (
        <div>
          <label>label</label>
          <Select
            options={labels}
            value={labelSearch}
            onChange={setLabelSearch}
          />
          <label>confidence</label>
          <input
            type="range"
            name="confidence"
            id="confidence"
            min={0}
            max={1}
            step={0.1}
            onChange={(e) => {
              setConfidence(e.target.value);
            }}
          />
          <button onClick={onClickFilter}>Filter</button>
        </div>
      )}
    </div>
  );
}

export default App;
