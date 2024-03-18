import React from "react";

function Loader() {
  return (
    <svg
      className="w-24 mx-auto mt-10"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 200 200"
    >
      <radialGradient
        id="a10"
        cx=".66"
        fx=".66"
        cy=".3125"
        fy=".3125"
        gradientTransform="scale(1.5)"
      >
        <stop offset="0" stopColor="#1B95FF"></stop>
        <stop offset=".3" stopColor="#1B95FF" stopOpacity=".9"></stop>
        <stop offset=".6" stopColor="#1B95FF" stopOpacity=".6"></stop>
        <stop offset=".8" stopColor="#1B95FF" stopOpacity=".3"></stop>
        <stop offset="1" stopColor="#1B95FF" stopOpacity="0"></stop>
      </radialGradient>
      <circle
        transform-origin="center"
        fill="none"
        stroke="url(#a10)"
        strokeWidth="15"
        strokeLinecap="round"
        strokeDasharray="200 1000"
        strokeDashoffset="0"
        cx="100"
        cy="100"
        r="70"
      >
        <animateTransform
          type="rotate"
          attributeName="transform"
          calcMode="spline"
          dur="2"
          values="360;0"
          keyTimes="0;1"
          keySplines="0 0 1 1"
          repeatCount="indefinite"
        ></animateTransform>
      </circle>
      <circle
        transform-origin="center"
        fill="none"
        opacity=".2"
        stroke="#1B95FF"
        strokeWidth="15"
        strokeLinecap="round"
        cx="100"
        cy="100"
        r="70"
      ></circle>
    </svg>
  );
}

export default Loader;
