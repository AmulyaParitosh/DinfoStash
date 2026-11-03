<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="brand/logo-lockup-dark-h256.png">
    <img src="brand/logo-lockup-h256.png" alt="DinfoStash" height="96">
  </picture>
</p>

<p align="center">
  Keep your whole career in one profile, and turn it into print-ready PDF resumes.
</p>

<p align="center">
  <a href="APP_URL"><b>Open DinfoStash</b></a>
</p>

---

DinfoStash is a web app for keeping one complete record of your work, and building as many
resumes from it as you need. Each resume has its own selection of content and its own
template; none of them ever changes the profile.

This repository is a showcase: it holds screenshots, example output and instructions. The
application's source code is private.

## What you can do

- **Keep one profile** of your jobs, projects, skills, education, achievements and contact
  details.
- **Import an existing resume** (PDF, LaTeX, plain text or JSON) instead of typing it all
  again. You review what was read, with a quality score for the result, before anything is
  saved.
- **Build several resumes** from the profile and keep them side by side, for example a
  backend version and a DevOps version.
- **Format text** with bold, italic, underline and links. No LaTeX knowledge needed.
- **Pick a template** and download a typeset PDF. The studio shows the real page count as
  you edit.
- **Tailor a resume to a job description** with AI. The rewrite fits what the chosen
  template prints, and points that add numbers your profile does not have are put back.
- **Edit your profile in plain language** with AI ("add my new job at…"). Changes are shown
  for review before they are saved, and earlier versions can be restored.
- **Save PDFs** to your account and share one by link.
- **Export or delete your account** yourself, from the Account page.

## Screenshots

<!-- TODO(TASK-101): take these from the deployed app with a fictional account, in light and dark. -->

| | Light | Dark |
| --- | --- | --- |
| Profile | ![Profile, light](screenshots/profile-light.png) | ![Profile, dark](screenshots/profile-dark.png) |
| Resume studio | ![Studio, light](screenshots/studio-light.png) | ![Studio, dark](screenshots/studio-dark.png) |
| Tailoring | ![Tailoring, light](screenshots/tailor-light.png) | ![Tailoring, dark](screenshots/tailor-dark.png) |

## Templates

Every template prints on A4. These examples are made from fictional profiles; the PDFs are
in [`examples/pdf`](examples/pdf).

| Classic single column | With a photo | Compact |
| --- | --- | --- |
| [![SingleColumnNoPhoto](examples/images/SingleColumnNoPhoto.jpg)](examples/pdf/SingleColumnNoPhoto.pdf) | [![SingleColumnPhoto](examples/images/SingleColumnPhoto.jpg)](examples/pdf/SingleColumnPhoto.pdf) | [![SingleColumnCompressed](examples/images/SingleColumnCompressed.jpg)](examples/pdf/SingleColumnCompressed.pdf) |

| Compact with a photo | Compact, refreshed layout | Bio-data (every profile field) |
| --- | --- | --- |
| [![SingleColumnPhotoCompressed](examples/images/SingleColumnPhotoCompressed.jpg)](examples/pdf/SingleColumnPhotoCompressed.pdf) | [![SingleColumnCompressedV2](examples/images/SingleColumnCompressedV2.jpg)](examples/pdf/SingleColumnCompressedV2.pdf) | [![Biodata](examples/images/Biodata.jpg)](examples/pdf/Biodata.pdf) |

<!-- TODO(TASK-101): add a tailoring example (fictional job description, before and after). -->

## Getting started

1. Open [DinfoStash](APP_URL) and sign up with your email or with Google.
2. Import an existing resume, or fill in your profile by hand.
3. Open **Resumes**, create a resume, pick a template and choose what to include.
4. Download the PDF, or save it to your account to share later.

AI features (import reading, tailoring, plain-language edits) are turned on per account.

## Privacy and terms

- [Privacy policy](APP_URL/privacy)
- [Terms of use](APP_URL/terms)

## Contact

Questions and feedback: [amulya1171@gmail.com](mailto:amulya1171@gmail.com)

## License

Copyright © 2024–2026 Amulya Paritosh. All rights reserved. See [LICENSE](LICENSE).
