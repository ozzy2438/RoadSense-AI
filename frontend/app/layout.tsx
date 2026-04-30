import "./globals.css";

export const metadata = {
  title: "RoadSense AI Console",
  description: "Operator console for agentic claims triage",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
