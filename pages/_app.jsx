import "../styles/global.css";
import { React } from "react";
export default function MyApp({ Component, pageProps }) {
  return (
    <div className="">
      <Component {...pageProps} />
    </div>
  );
}
