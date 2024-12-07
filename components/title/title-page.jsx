import { Helmet } from "react-helmet";
export default function TitlePage({ titleIndex }) {
  return (
    <Helmet>
      <link
        rel="icon"
        href="https://st.gismeteo.st/ui-gm/assets/meta/favicon-32x32.png"
      />
      <link
        rel="icon"
        type="image/png"
        href="https://st.gismeteo.st/ui-gm/assets/meta/favicon-16x16.png"
      />

      <title>{titleIndex}</title>
    </Helmet>
  );
}
