// frontend/src/components/SkillSelector.jsx
export default function SkillSelector({
	skills,
	selectedSkill,
	setSelectedSkill,
}) {
	return (
		<div>
			<label
				htmlFor="skill-select"
				className="block text-sm font-medium text-gray-400 mb-2"
			>
				Select a Skill
			</label>
			<select
				id="skill-select"
				value={selectedSkill}
				onChange={(e) => setSelectedSkill(e.target.value)}
				className="w-full bg-[#1c1c1c] border border-gray-700 rounded-md p-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
			>
				{skills.map((skill) => (
					<option key={skill} value={skill}>
						{skill}
					</option>
				))}
			</select>
		</div>
	);
}
