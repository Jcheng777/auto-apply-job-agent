"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Plus, Trash } from "lucide-react";

export default function ApplicationsPage() {
  const [urls, setUrls] = useState([{ url: "", title: "" }]);

  const handleUrlChange = (idx: number, field: string, value: string) => {
    setUrls((prev) => {
      const copy = [...prev];
      copy[idx][field] = value;
      return copy;
    });
  };

  const addUrl = () => setUrls((prev) => [...prev, { url: "", title: "" }]);
  const removeUrl = (idx: number) =>
    setUrls((prev) => prev.filter((_, i) => i !== idx));

  return (
    <div className="max-w-2xl mx-auto py-10">
      <Card>
        <CardHeader>
          <CardTitle>Job Application URLs</CardTitle>
          <p className="text-sm text-muted-foreground">
            Add one or more job application URLs to process
          </p>
        </CardHeader>
        <CardContent>
          {urls.map((entry, idx) => (
            <div key={idx} className="flex gap-2 mb-2 items-center">
              <Input
                placeholder="https://company.com/jobs/apply/..."
                value={entry.url}
                onChange={(e) => handleUrlChange(idx, "url", e.target.value)}
                className="flex-1"
              />
              <Input
                placeholder="Software Engineer at Company"
                value={entry.title}
                onChange={(e) => handleUrlChange(idx, "title", e.target.value)}
                className="flex-1"
              />
              {urls.length > 1 && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => removeUrl(idx)}
                >
                  <Trash className="w-4 h-4" />
                </Button>
              )}
            </div>
          ))}
          <Button variant="outline" className="w-full mb-4" onClick={addUrl}>
            <Plus className="w-4 h-4 mr-2" /> Add Another URL
          </Button>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <Button variant="outline">Extract Fields Only</Button>
            <Button variant="secondary">Fill Forms (No Submit)</Button>
            <Button variant="default">Fill & Submit Forms</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
