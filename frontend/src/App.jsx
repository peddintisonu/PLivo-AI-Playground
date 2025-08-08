// frontend/src/App.jsx
import {
	SignedIn,
	SignedOut,
	SignInButton,
	UserButton,
} from "@clerk/clerk-react";
import Playground from "./components/Playground"; // We will create this next

function App() {
	return (
		<div className="bg-[#0a0a0a] text-gray-200 min-h-screen font-sans">
			<header className="flex justify-between items-center p-4 border-b border-gray-800">
				<h1 className="text-xl font-bold">{import.meta.env.VITE_APP_NAME || "Plivo AI Playground"}</h1>
				<div>
					<SignedOut>
						<div className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
							<SignInButton />
						</div>
					</SignedOut>
					<SignedIn>
						<UserButton />
					</SignedIn>
				</div>
			</header>

			<main className="p-4 md:p-8">
				<SignedIn>
					<Playground />
				</SignedIn>
				<SignedOut>
					<div className="text-center mt-20">
						<h2 className="text-2xl font-semibold">
							Welcome to the AI Playground
						</h2>
						<p className="text-gray-400 mt-2">
							Please sign in to access the tools.
						</p>
					</div>
				</SignedOut>
			</main>
		</div>
	);
}

export default App;
