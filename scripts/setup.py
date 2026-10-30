"""Install a checked-out snapshot; existing project content is never replaced."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

BEGIN = '<!-- project-collaboration-skill:begin -->'
END = '<!-- project-collaboration-skill:end -->'


def inside(root, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('Expected a project-relative path: ' + str(relative))
    result = (root / path).resolve()
    if result == root or root not in result.parents:
        raise ValueError('Path escapes project: ' + str(relative))
    return result


def install(project, source, consensus='docs/CollaborationConsensus.md', learning='docs/learning', revision=None):
    project, source = Path(project).resolve(), Path(source).resolve()
    if not project.is_dir():
        raise ValueError('Project directory must already exist')
    consensus_path = inside(project, consensus)
    inside(project, learning)
    agents = inside(project, 'AGENTS.md')
    if (project / 'AGENT.md').exists() and not agents.exists():
        raise ValueError('Existing AGENT.md: merge the entry manually before installation')
    pending = {}
    hashes = {}
    for name in ('shared-understanding', 'adaptive-teaching'):
        data = (source / 'skills' / name / 'SKILL.md').read_bytes()
        dest = inside(project, '.agents/skills/' + name + '/SKILL.md')
        hashes[name] = hashlib.sha256(data).hexdigest()
        if dest.exists():
            if dest.read_bytes() != data:
                raise ValueError('Existing Skill differs; merge explicitly: ' + str(dest))
        else:
            pending[dest] = data
    rules = (source / 'templates/AGENTS.md').read_text(encoding='utf-8').strip()
    rules = rules.replace('{{consensus}}', Path(consensus).as_posix()).replace('{{learning}}', Path(learning).as_posix())
    block = BEGIN + '\n' + rules + '\n' + END
    original = agents.read_bytes() if agents.exists() else b''
    if BEGIN.encode() in original or END.encode() in original:
        if block.encode('utf-8') not in original:
            raise ValueError('Existing managed entry differs; merge explicitly')
    else:
        pending[agents] = original + (b'\n\n' if original else b'') + block.encode('utf-8') + b'\n'
    if not consensus_path.exists():
        pending[consensus_path] = (source / 'templates/CollaborationConsensus.md').read_bytes()
    elif not consensus_path.is_file():
        raise ValueError('Consensus path is not a file')
    if revision is None:
        revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    receipt = inside(project, '.collaboration-kit-source.json')
    if not receipt.exists():
        pending[receipt] = (json.dumps({'repository': 'https://github.com/throusea/project-collaboration-skill', 'revision': revision, 'skills_sha256': hashes, 'consensus': consensus, 'learning': learning}, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    # Preflight all destinations before the first write. Exclusive creates avoid
    # replacing another window's new file; the AGENTS append checks its snapshot.
    for path in pending:
        if path.exists() and path != agents:
            raise ValueError('Destination appeared during preflight: ' + str(path))
    written = []
    for path, data in pending.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if path == agents and path.exists():
            if path.read_bytes() != original:
                raise ValueError('AGENTS changed during installation; rerun after review')
            with path.open('ab') as stream:
                stream.write(data[len(original):])
        else:
            with path.open('xb') as stream:
                stream.write(data)
        written.append(str(path.relative_to(project)))
    return written


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('--consensus', default='docs/CollaborationConsensus.md')
    parser.add_argument('--learning', default='docs/learning')
    parser.add_argument('--revision', help='Full source SHA when using a downloaded snapshot without .git')
    args = parser.parse_args()
    try:
        changes = install(args.project, Path(__file__).resolve().parents[1], args.consensus, args.learning, args.revision)
        print(json.dumps({'created_or_extended': changes}, ensure_ascii=False, indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, str(error) + '\n')
