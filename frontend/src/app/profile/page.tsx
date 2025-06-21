"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

const initialProfile = {
  name: "",
  email: "",
  phone: "",
  website: "",
  linkedin: "",
  github: "",
  desiredSalary: "",
  yearsExperience: "",
  address: "",
  summary: "",
};

export default function ProfilePage() {
  const [profile, setProfile] = useState(initialProfile);

  const handleChange = (field: string, value: string) => {
    setProfile((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    // TODO: Integrate with backend
    alert("Profile saved (not yet integrated)");
  };

  return (
    <div className="max-w-2xl mx-auto py-10">
      <Card>
        <CardHeader>
          <CardTitle>User Profile</CardTitle>
          <p className="text-sm text-muted-foreground">
            Configure your personal information for form filling
          </p>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <Input
              placeholder="Full Name"
              value={profile.name}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleChange("name", e.target.value)
              }
            />
            <Input
              placeholder="Email"
              value={profile.email}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleChange("email", e.target.value)
              }
            />
            <Input
              placeholder="Phone"
              value={profile.phone}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleChange("phone", e.target.value)
              }
            />
            <Input
              placeholder="LinkedIn"
              value={profile.linkedin}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleChange("linkedin", e.target.value)
              }
            />
            <Input
              placeholder="Website"
              value={profile.website}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleChange("website", e.target.value)
              }
            />
            <Input
              placeholder="GitHub"
              value={profile.github}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleChange("github", e.target.value)
              }
            />
            <Input
              placeholder="Desired Salary"
              value={profile.desiredSalary}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleChange("desiredSalary", e.target.value)
              }
            />
            <Input
              placeholder="Years of Experience"
              value={profile.yearsExperience}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleChange("yearsExperience", e.target.value)
              }
            />
            <Input
              placeholder="Address"
              value={profile.address}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleChange("address", e.target.value)
              }
              className="md:col-span-2"
            />
          </div>
          <Textarea
            placeholder="Professional Summary"
            value={profile.summary}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
              handleChange("summary", e.target.value)
            }
            className="mb-4"
          />
          <div className="flex gap-2">
            <Button onClick={handleSave}>Save Profile</Button>
            <Button variant="outline">Load from File</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
