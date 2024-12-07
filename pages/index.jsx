import { React } from "react";
import TitlePage from "../components/title/title-page";
import { YandexMap } from "@/components/map/yandex-map";
import { Header } from "@/components/header";
export default function HomePage() {
  return (
    <HomePageLayout titlePage={<TitlePage titleIndex="ЙОУУУУ" />}>
      <YandexMap />
    </HomePageLayout>
  );
}

function HomePageLayout({ titlePage, children }) {
  return (
    <>
      {titlePage}
      <main className="">{children}</main>
    </>
  );
}
