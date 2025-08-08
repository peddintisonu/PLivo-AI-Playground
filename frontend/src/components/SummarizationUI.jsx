// frontend/src/components/SummarizationUI.jsx
import { useState } from "react";
import axios from "axios";
// import { useAuth } from "@clerk/clerk-react"; // Temporarily disabled for testing
import { Upload, Link } from "lucide-react";

const API_URL = `${import.meta.env.VITE_API_BASE_URL}/summarize`;

// The props setIsLoading, setOutput, setError are passed down from Playground.jsx
export default function SummarizationUI({ setIsLoading, setOutput, setError }) {
	const [inputType, setInputType] = useState("URL");
	const [url, setUrl] = useState("");
	const [file, setFile] = useState(null);
	// const { getToken } = useAuth(); // Temporarily disabled for testing

	// Create a local loading state just for this component's UI
	const [isComponentLoading, setIsComponentLoading] = useState(false);

	const handleSubmit = async (e) => {
		e.preventDefault();
		if ((inputType === "URL" && !url) || (inputType === "File" && !file)) {
			setError("Please provide a URL or a file.");
			return;
		}

		// Set both the parent and local loading states to true
		setIsLoading(true);
		setIsComponentLoading(true);
		setOutput(null);
		setError("");

		const formData = new FormData();
		formData.append("inputType", inputType);
		if (inputType === "URL") {
			formData.append("url", url);
		} else {
			formData.append("file", file);
		}

		try {
			// Temporarily remove auth for testing
			const response = await axios.post(API_URL, formData, {
				headers: {
					"Content-Type": "multipart/form-data",
				},
			});
			setOutput(response.data);
		} catch (err) {
			if (err.response?.status === 503) {
				setError("The AI service is temporarily overloaded. Please try again in a few minutes.");
			} else {
				setError(err.response?.data?.detail || "An error occurred during summarization.");
			}
		} finally {
			// Set both the parent and local loading states to false
			setIsLoading(false);
			setIsComponentLoading(false);
		}
	};

	return (
		<form onSubmit={handleSubmit} className="space-y-4">
			<div className="flex items-center space-x-4">
				<label className="flex items-center space-x-2 cursor-pointer">
					<input
						type="radio"
						name="inputType"
						value="URL"
						checked={inputType === "URL"}
						onChange={() => setInputType("URL")}
						className="form-radio bg-gray-800 border-gray-600 text-blue-500"
					/>
					<span className="text-gray-300">URL</span>
				</label>
				<label className="flex items-center space-x-2 cursor-pointer">
					<input
						type="radio"
						name="inputType"
						value="File"
						checked={inputType === "File"}
						onChange={() => setInputType("File")}
						className="form-radio bg-gray-800 border-gray-600 text-blue-500"
					/>
					<span className="text-gray-300">File (PDF/DOCX)</span>
				</label>
			</div>

			{inputType === "URL" ? (
				<div className="relative">
					<Link
						className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500"
						size={20}
					/>
					<input
						type="url"
						placeholder="https://example.com/article"
						value={url}
						onChange={(e) => setUrl(e.target.value)}
						className="w-full pl-10 pr-3 py-2 bg-[#1c1c1c] border border-gray-700 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none"
					/>
				</div>
			) : (
				<div>
					<label
						htmlFor="file-upload"
						className="relative cursor-pointer bg-[#1c1c1c] border-2 border-dashed border-gray-600 rounded-md flex justify-center items-center w-full h-24 hover:border-gray-500"
					>
						<div className="flex flex-col items-center">
							<Upload className="text-gray-500" size={24} />
							<span className="mt-1 text-sm text-gray-400">
								{file ? file.name : "Click to upload"}
							</span>
						</div>
						<input
							id="file-upload"
							type="file"
							className="sr-only"
							accept=".pdf,.docx"
							onChange={(e) => setFile(e.target.files[0])}
						/>
					</label>
				</div>
			)}

			<button
				type="submit"
				className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition-colors disabled:bg-gray-600 disabled:cursor-not-allowed"
				disabled={isComponentLoading} // <-- FIXED: Use the local loading state here
			>
				{isComponentLoading ? "Summarizing..." : "Generate Summary"}
			</button>
		</form>
	);
}
