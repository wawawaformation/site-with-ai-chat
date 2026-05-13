import "./globals.css";

export const metadata = {
  title: "Carnet de recettes",
  description: "Mini-app de recettes avec chat IA",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
