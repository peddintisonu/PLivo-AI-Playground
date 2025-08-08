import { useState } from "react";
import axios from "axios";
import { Upload, Mic } from "lucide-react";

const API_URL = `${import.meta.env.VITE_API_BASE_URL}/analyze-conversation`;

export default function ConversationAnalysisUI({ setIsLoading, setOutput, setError }) {
	const [audioFile, setAudioFile] = useState(null);
	const [isComponentLoading, setIsComponentLoading] = useState(false);

	const handleFileChange = (e) => {
		const file = e.target.files[0];
		if (file) {
			setAudioFile(file);
			setError("");
		}
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		if (!audioFile) {
			setError("Please select an audio file.");
			return;
		}

		setIsLoading(true);
		setIsComponentLoading(true);
		setOutput(null);
		setError("");

		const formData = new FormData();
		formData.append("audio", audioFile);

		try {
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
				setError(err.response?.data?.detail || "An error occurred during conversation analysis.");
			}
		} finally {
			setIsLoading(false);
			setIsComponentLoading(false);
		}
	};

	return (
		<form onSubmit={handleSubmit} className="space-y-4">
			<div>
				<label
					htmlFor="audio-upload"
					className="relative cursor-pointer bg-[#1c1c1c] border-2 border-dashed border-gray-600 rounded-md flex justify-center items-center w-full h-32 hover:border-gray-500"
				>
					<div className="flex flex-col items-center">
						<Mic className="text-gray-500" size={32} />
						<span className="mt-2 text-sm text-gray-400">
							{audioFile ? audioFile.name : "Click to upload an audio file"}
						</span>
						<span className="mt-1 text-xs text-gray-500">
							MP3, WAV, M4A, FLAC
						</span>
					</div>
					<input
						id="audio-upload"
						type="file"
						className="sr-only"
						accept="audio/*"
						onChange={handleFileChange}
					/>
				</label>
			</div>

			{audioFile && (
				<div className="p-4 bg-[#1c1c1c] border border-gray-700 rounded-md">
					<p className="text-sm text-gray-400 mb-2">Selected Audio:</p>
					<div className="flex items-center space-x-2">
						<Mic size={16} className="text-blue-400" />
						<span className="text-sm text-gray-300">{audioFile.name}</span>
						<span className="text-xs text-gray-500">
							({(audioFile.size / 1024 / 1024).toFixed(2)} MB)
						</span>
					</div>
				</div>
			)}

			<button
				type="submit"
				className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition-colors disabled:bg-gray-600 disabled:cursor-not-allowed"
				disabled={isComponentLoading}
			>
				{isComponentLoading ? "Processing Audio..." : "Analyze Conversation"}
			</button>
		</form>
	);
}
