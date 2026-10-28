<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class PlaybookTest extends TestCase
{
    public function test_signup_emails_the_playbook_and_a_note_and_rejects_bad_input(): void
    {
        config(['mail.to' => 'owner@example.com']);
        $sent = fn () => Mail::mailer()->getSymfonyTransport()->messages()->map->getOriginalMessage();

        $this->postJson('/api/playbook', ['email' => 'not-an-email', 'trade' => 'roofing', 'consent' => true])->assertStatus(422);
        $this->postJson('/api/playbook', ['email' => 'jo@example.com', 'trade' => 'roofing', 'consent' => false])->assertStatus(422);
        $this->postJson('/api/playbook', ['email' => 'jo@example.com', 'trade' => '../../.env', 'consent' => true])->assertStatus(422);
        $this->assertCount(0, $sent());

        $this->postJson('/api/playbook', ['email' => 'jo@example.com', 'trade' => 'roofing', 'consent' => true])->assertNoContent();

        [$playbook, $note] = $sent()->all();
        $this->assertSame('jo@example.com', $playbook->getTo()[0]->getAddress());
        $this->assertSame('owner@example.com', $playbook->getReplyTo()[0]->getAddress());
        $this->assertSame('Your free Roofing playbook', $playbook->getSubject());
        $this->assertSame('roofing.pdf', $playbook->getAttachments()[0]->getFilename());
        $this->assertStringContainsString('unsubscribe', $playbook->getTextBody());
        $this->assertSame('owner@example.com', $note->getTo()[0]->getAddress());
        $this->assertSame('jo@example.com', $note->getReplyTo()[0]->getAddress());
        $this->assertSame('Free playbook: Roofing', $note->getSubject());

        // A second request the same day only sends you a note, so the form can't flood an inbox.
        $this->postJson('/api/playbook', ['email' => 'JO@example.com', 'trade' => 'hvac', 'consent' => true])->assertNoContent();
        $this->assertCount(3, $sent());
        $this->assertSame('owner@example.com', $sent()->last()->getTo()[0]->getAddress());
        $this->assertStringContainsString('wasn\'t sent', $sent()->last()->getTextBody());
    }

    // Every trade in T has a playbook and its PDF (`php artisan playbooks` makes the PDFs).
    public function test_every_trade_has_a_playbook(): void
    {
        preg_match_all('/^\{s:"([a-z-]+)"/m', file_get_contents(resource_path('views/home.blade.php')), $trades);
        $this->assertNotEmpty($trades[1]);

        foreach ($trades[1] as $slug) {
            $this->assertFileExists(base_path("playbooks/$slug.md"));
            $this->assertFileExists(public_path("playbooks/$slug.pdf"));
            $this->assertStringContainsString("followthroughguides.com/$slug\"", file_get_contents(base_path("playbooks/$slug.md")));
        }
    }
}
