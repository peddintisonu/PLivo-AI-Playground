import { useState } from "react";
import axios from "axios";
import { Upload, MessageSquare } from "lucide-react";

const API_URL = `${import.meta.env.VITE_API_BASE_URL}/analyze-image`;

export default function ImageAnalysisUI({ setIsLoading, setOutput, setError }) {
	const [imageFile, setImageFile] = useState(null);
	const [prompt, setPrompt] = useState("");
	const [previewUrl, setPreviewUrl] = useState("");
	const [isComponentLoading, setIsComponentLoading] = useState(false);

	const handleFileChange = (e) => {
		const file = e.target.files[0];
		if (file) {
			setImageFile(file);
			setPreviewUrl(URL.createObjectURL(file));
			setError("");
		}
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		if (!imageFile) {
			setError("Please select an image file.");
			return;
		}

		setIsLoading(true);
		setIsComponentLoading(true);
		setOutput(null);
		setError("");

		const formData = new FormData();
		formData.append("image", imageFile);
		formData.append("prompt", prompt || "Analyze this image and describe what you see in detail.");

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
				setError(err.response?.data?.detail || "An error occurred during image analysis.");
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
					htmlFor="image-upload"
					className="relative cursor-pointer bg-[#1c1c1c] border-2 border-dashed border-gray-600 rounded-md flex justify-center items-center w-full h-32 hover:border-gray-500"
				>
					<div className="flex flex-col items-center">
						<Upload className="text-gray-500" size={32} />
						<span className="mt-2 text-sm text-gray-400">
							{imageFile ? imageFile.name : "Click to upload an image"}
						</span>
						<span className="mt-1 text-xs text-gray-500">
							PNG, JPG, JPEG, WebP
						</span>
					</div>
					<input
						id="image-upload"
						type="file"
						className="sr-only"
						accept="image/*"
						onChange={handleFileChange}
					/>
				</label>
			</div>

			{previewUrl && (
				<div className="p-4 bg-[#1c1c1c] border border-gray-700 rounded-md">
					<p className="text-sm text-gray-400 mb-2">Preview:</p>
					<img
						src={previewUrl}
						alt="Preview"
						className="max-w-full h-48 object-contain rounded border border-gray-600"
					/>
				</div>
			)}

			<div className="relative">
				<MessageSquare
					className="absolute left-3 top-3 text-gray-500"
					size={20}
				/>
				<textarea
					placeholder="Enter your analysis prompt (optional). Default: Analyze this image and describe what you see in detail."
					value={prompt}
					onChange={(e) => setPrompt(e.target.value)}
					className="w-full pl-10 pr-3 py-2 bg-[#1c1c1c] border border-gray-700 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none"
					rows="3"
				/>
			</div>

			<button
				type="submit"
				className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition-colors disabled:bg-gray-600 disabled:cursor-not-allowed"
				disabled={isComponentLoading}
			>
				{isComponentLoading ? "Analyzing..." : "Analyze Image"}
			</button>
		</form>
	);
}
