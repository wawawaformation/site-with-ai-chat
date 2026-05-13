"use client";

import { useState } from "react";
import RecipeList from "@/components/RecipeList";
import ChatPanel from "@/components/ChatPanel";

export default function Home() {
  const [refreshSignal, setRefreshSignal] = useState(0);
  const triggerRefresh = () => setRefreshSignal((k) => k + 1);

  return (
    <main className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Carnet de recettes</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <section>
          <RecipeList refreshSignal={refreshSignal} />
        </section>
        <section>
          <ChatPanel onMutation={triggerRefresh} />
        </section>
      </div>
    </main>
  );
}
